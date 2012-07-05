import os
import sys
from zope.component import getSiteManager
from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
import pyramid_zcml
from events import AppRootReady
from w20e.forms.registry import Registry
from w20e.forms.pyramid.file import PyramidFile
from models.imagefolder import ImageFolder
from pack import PackCommand
from migration import migrate


Registry.register_renderable("file", PyramidFile)
Registry.set_html_template_path("./bootstrap")

here = os.path.abspath(os.path.dirname(__file__))
version = open(os.path.join(here, "version.txt")
               ).readlines()[0].strip()


def class_from_string(clazz_name):

    """ We'll need to follow the dotted path, and find the module that
    starts with some part, and provides the rest of the path... """

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

    """ Any updates can go here... """

    curr_version = getattr(app, "pycms_version", "unknown")
    tgt_version = version

    if curr_version != tgt_version:

        migrated = migrate(curr_version, tgt_version)

        if migrated:
            setattr(app, "pycms_version", tgt_version)


def appmaker(config):

    """ Create the application. Call this method from your main Pyramid
    setup """

    initreq = InitRequest()
    initreq.registry = config.registry

    conn = get_connection(initreq)

    zodb_root = conn.root()

    if not 'app_root' in zodb_root:

        root_clazz_name = config.registry.settings.get("pycms.rootclass",
                                           "w20e.pycms.models.site.Site")
        root_title = config.registry.settings.get("pycms.roottitle",
                                           "Yet another PyCMS app!")


        root_clazz = class_from_string(root_clazz_name)

        app_root = root_clazz("root")
        app_root.__data__['name'] = root_title
        app_root.__parent__ = app_root.__name__ = None

        setattr(app_root, 'pycms_version', version)

        zodb_root['app_root'] = app_root

        import transaction
        transaction.commit()

    # create a globale images folder
    app_root = zodb_root['app_root']
    IMAGES_ID = 'images'
    if not IMAGES_ID in app_root:
        images = ImageFolder(IMAGES_ID)
        images.__data__['name'] = 'Images'
        app_root.add_content(images)
        import transaction
        transaction.commit()

    # Do necessary updates
    update(zodb_root['app_root'])

    initreq.registry.notify(AppRootReady(app_root, config.registry))

    import transaction
    transaction.commit()

    return zodb_root['app_root']


def root_factory(request):

    conn = get_connection(request)

    return conn.root()['app_root']


def make_pycms_app(app, **settings):
    
    """ Create a w20e.pycms application and return it. The app is a
    router instance as created by Configurator.make_wsgi_app."""
    
    config = Configurator(package=app,
                          root_factory=root_factory,
                          settings=settings)

    def get_registry():

        return config.registry

    # hook up registry
    getSiteManager.sethook(get_registry)    

    config.include(pyramid_zcml)
    config.include('pyramid_mailer')

    config.load_zcml('w20e.pycms:bootstrap.zcml')
    config.commit()
    
    config.load_zcml("configure.zcml")
    config.commit()

    appmaker(config)

    getSiteManager.reset()
    config.hook_zca()

    return config.make_wsgi_app()
