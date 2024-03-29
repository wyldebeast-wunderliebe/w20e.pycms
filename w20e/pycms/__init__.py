
import os
import sys
import transaction
from zope.component import getSiteManager
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
import pkg_resources
from functools import reduce
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid_authstack import AuthenticationStackPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder
from pyramid_jwt.policy import JWTAuthenticationPolicy


Registry.register_renderable("file", PyramidFile)

tpl_path = os.path.join(os.path.dirname(__file__), "templates/w20e_forms_overrides/")
Registry.add_html_template_path(tpl_path)
Registry.add_html_template_path("./bootstrap")

here = os.path.abspath(os.path.dirname(__file__))
version = pkg_resources.get_distribution("w20e.pycms").version


def class_from_string(clazz_name):
    """We'll need to follow the dotted path, and find the module that
    starts with some part, and provides the rest of the path..."""

    clazz_path = clazz_name.split(".")

    if len(clazz_path) == 1:
        mod_name = __name__
        clazz = clazz_name
    else:
        if ".".join(clazz_path[:-1]) in sys.modules:
            mod_name = ".".join(clazz_path[:-1])
            clazz = clazz_path[-1]
        else:
            mod_name = ".".join(clazz_path[:-2])
            clazz = ".".join(clazz_path[-2:])
            __import__(".".join(clazz_path[:-1]))

    return reduce(getattr, clazz.split("."), sys.modules[mod_name])


class InitRequest(object):
    registry = None
    cb = None

    def add_finished_callback(self, cb):
        self.cb = cb


def update(app):
    """Any updates can go here..."""

    curr_version = getattr(app, "pycms_version", "unknown")
    tgt_version = version

    if curr_version != tgt_version:
        migrated = migrate(curr_version, tgt_version)

        if migrated:
            setattr(app, "pycms_version", tgt_version)


def appmaker(config, zodb_root=None):
    """Create the application. Call this method from your main Pyramid
    setup"""
    initreq = InitRequest()
    initreq.registry = config.registry

    if not zodb_root:
        conn = get_connection(initreq)
        zodb_root = conn.root()

    if not "app_root" in zodb_root:
        root_clazz_name = config.registry.settings.get(
            "pycms.rootclass", "w20e.pycms.models.site.Site"
        )
        root_title = config.registry.settings.get(
            "pycms.roottitle", "Yet another w20e.pycms app!"
        )

        root_clazz = class_from_string(root_clazz_name)

        app_root = root_clazz("root")
        app_root._data_["name"] = root_title
        app_root.__parent__ = app_root.__name__ = None

        setattr(app_root, "pycms_version", version)

        zodb_root["app_root"] = app_root

        transaction.commit()

    app_root = zodb_root["app_root"]

    # Do necessary updates
    update(zodb_root["app_root"])
    initreq.registry.notify(AppRootReady(app_root, config.registry))
    transaction.commit()

    #  create a globale images folder
    IMAGES_ID = "images"
    if not IMAGES_ID in app_root:
        images = ImageFolder(IMAGES_ID)
        images._data_["name"] = "Images"
        app_root.add_content(images)
        transaction.commit()

    return zodb_root["app_root"]


def root_factory(request):
    conn = get_connection(request)

    return conn.root()["app_root"]


def make_pycms_app(app, *includes, **settings):
    """Create a w20e.pycms application and return it. The app is a
    router instance as created by Configurator.make_wsgi_app."""
    config = Configurator(
        package=app,
        root_factory=root_factory,
        session_factory=SessionFactory("w20e_pycms_secret"),
        settings=settings,
    )

    # securiy policies
    auth_policy = AuthenticationStackPolicy()
    auth_policy.add_policy(
        "cookie", AuthTktAuthenticationPolicy(secret="evilsecret", callback=groupfinder)
    )

    # Enable JWT authentication.
    config.include("pyramid_jwt")

    jwt_policy = JWTAuthenticationPolicy("evilsecret2", callback=groupfinder)

    auth_policy.add_policy("token", jwt_policy)

    def request_create_token(
        request, principal, expiration=None, audience=None, **claims
    ):
        return jwt_policy.create_token(principal, expiration, audience, **claims)

    def request_claims(request):
        return jwt_policy.get_claims(request)

    config.add_request_method(request_create_token, "create_jwt_token")
    config.add_request_method(request_claims, "jwt_claims", reify=True)

    config.set_authentication_policy(auth_policy)
    auth_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(auth_policy)

    # enable Chameleon rendering
    #
    config.include("pyramid_chameleon")

    register_json_adapters(config)

    def get_registry(*args):
        return config.registry

    # hook up registry
    #
    getSiteManager.sethook(get_registry)

    config.include(pyramid_zcml)

    config.load_zcml("w20e.pycms:bootstrap.zcml")

    config.scan("w20e.pycms")
    config.commit()
    config.load_zcml("configure.zcml")
    config.commit()

    # Other includes
    #
    for include in includes:
        config.include(include)

    # load pycms_prerequisites
    for ep in pkg_resources.iter_entry_points(group="pycms_prerequisite_plugin"):
        fun = ep.load()
        config.include(fun)
        config.commit()

    # load plugin entry points of the pycms_plugin persuasion
    for ep in pkg_resources.iter_entry_points(group="pycms_plugin"):
        fun = ep.load()
        config.include(fun)
        config.commit()
    config.commit()

    appmaker(config)

    return config.make_wsgi_app()
