import os
import sys
import transaction
from functools import reduce
from zope.component import getSiteManager
from importlib.metadata import version, PackageNotFoundError, entry_points
from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from pyramid.session import SignedCookieSessionFactory as SessionFactory
import pyramid_zcml
from .events import AppRootReady
from w20e.forms.registry import Registry
from w20e.forms.pyramid.file import PyramidFile
from .models.imagefolder import ImageFolder
from .json_adapters import register_json_adapters
from .migration import migrate
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid_authstack import AuthenticationStackPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder
from pyramid_jwt.policy import JWTAuthenticationPolicy


# Fetch version dynamically
try:
    __version__ = version("w20e.pycms")
except PackageNotFoundError:
    __version__ = "unknown"

# Register Pyramid form components
Registry.register_renderable("file", PyramidFile)

tpl_path = os.path.join(os.path.dirname(__file__), "templates/w20e_forms_overrides/")
Registry.add_html_template_path(tpl_path)
Registry.add_html_template_path("./bootstrap")


def class_from_string(clazz_name):
    """Resolve a class from its full dotted string path."""
    clazz_path = clazz_name.split(".")

    if len(clazz_path) == 1:
        return getattr(sys.modules[__name__], clazz_name)

    module_name = ".".join(clazz_path[:-1])
    clazz = clazz_path[-1]

    if module_name not in sys.modules:
        __import__(module_name)

    return reduce(getattr, clazz.split("."), sys.modules[module_name])


class InitRequest:
    """Request mock for initialization purposes."""
    registry = None
    cb = None

    def add_finished_callback(self, cb):
        self.cb = cb


def update(app):
    """Perform any required migrations."""
    curr_version = getattr(app, "pycms_version", "unknown")

    if curr_version != __version__:
        if migrate(curr_version, __version__):
            setattr(app, "pycms_version", __version__)


def appmaker(config, zodb_root=None):
    """Create the application and initialize if needed."""
    initreq = InitRequest()
    initreq.registry = config.registry

    if not zodb_root:
        conn = get_connection(initreq)
        zodb_root = conn.root()

    if "app_root" not in zodb_root:
        root_class_name = config.registry.settings.get(
            "pycms.rootclass", "w20e.pycms.models.site.Site"
        )
        root_title = config.registry.settings.get(
            "pycms.roottitle", "Yet another w20e.pycms app!"
        )

        root_class = class_from_string(root_class_name)
        app_root = root_class("root")
        app_root._data_["name"] = root_title
        app_root.__parent__ = app_root.__name__ = None

        setattr(app_root, "pycms_version", __version__)
        zodb_root["app_root"] = app_root
        transaction.commit()

    app_root = zodb_root["app_root"]
    update(app_root)
    initreq.registry.notify(AppRootReady(app_root, config.registry))
    transaction.commit()

    # Create a global images folder if not present
    if "images" not in app_root:
        images = ImageFolder("images")
        images._data_["name"] = "Images"
        app_root.add_content(images)
        transaction.commit()

    return app_root


def root_factory(request):
    """Return the application root."""
    return get_connection(request).root()["app_root"]


def make_pycms_app(app, *includes, **settings):
    """Create and configure the Pyramid app."""
    
    # Use settings for secret keys instead of hardcoded values
    session_secret = settings.get("pycms.session_secret", "default_session_secret")
    auth_cookie_secret = settings.get("pycms.auth_cookie_secret", "default_auth_secret")
    jwt_secret = settings.get("pycms.jwt_secret", "default_jwt_secret")

    config = Configurator(
        package=app,
        root_factory=root_factory,
        session_factory=SessionFactory(session_secret),  # Now configurable
        settings=settings,
    )

    # Authentication setup
    auth_policy = AuthenticationStackPolicy()

    auth_policy.add_policy(
        "cookie",
        AuthTktAuthenticationPolicy(
            secret=auth_cookie_secret,  # Now configurable
            callback=groupfinder
        ),
    )

    config.include("pyramid_jwt")
    jwt_policy = JWTAuthenticationPolicy(
        jwt_secret,  # Now configurable
        callback=groupfinder
    )

    auth_policy.add_policy("token", jwt_policy)
    config.add_request_method(jwt_policy.create_token, "create_jwt_token")
    config.add_request_method(jwt_policy.get_claims, "jwt_claims", reify=True)

    config.set_authentication_policy(auth_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())

    # Include Chameleon rendering
    config.include("pyramid_chameleon")

    # Register JSON adapters
    register_json_adapters(config)

    # Hook up registry
    getSiteManager.sethook(lambda *args: config.registry)

    # Load ZCML if required
    config.include(pyramid_zcml)
    config.load_zcml("w20e.pycms:bootstrap.zcml")

    config.scan("w20e.pycms")
    config.commit()
    config.load_zcml("configure.zcml")
    config.commit()

    # Include additional modules
    for include in includes:
        config.include(include)

    # Load prerequisite plugins using `importlib.metadata`
    try:
        for ep in entry_points(group="pycms_prerequisite_plugin"):
            config.include(ep.load())
            config.commit()
    except Exception as e:
        print(f"Failed to load prerequisite plugins: {e}")

    # Load core plugins using `importlib.metadata`
    try:
        for ep in entry_points(group="pycms_plugin"):
            config.include(ep.load())
            config.commit()
    except Exception as e:
        print(f"Failed to load core plugins: {e}")

    appmaker(config)

    return config.make_wsgi_app()

