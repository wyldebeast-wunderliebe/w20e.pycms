import os
from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
import pyramid_zcml
from events import AppRootReady
from w20e.forms.registry import Registry
from w20e.forms.pyramid.file import PyramidFile

Registry.register_renderable("file", PyramidFile)

here = os.path.abspath(os.path.dirname(__file__))
version = open(os.path.join(here, "version.txt")
               ).readlines()[0].strip()


class InitRequest(object):

    registry = None
    cb = None

    def add_finished_callback(self, cb):
        self.cb = cb


def update(app):

    """ Any updates can go here... """


def appmaker(config):

    initreq = InitRequest()
    initreq.registry = config.registry

    conn = get_connection(initreq)

    zodb_root = conn.root()

    if not 'app_root' in zodb_root:

        root_clazz = registry.settings.get("pycms.rootclass",
                                           "w20e.pycms.models.site.Site")
        root_title = registry.settings.get("pycms.roottitle",
                                           "Welcome")
        app_root = root_clazz(root_title)
        app_root.__data__['name'] = 'welcome'
        app_root.__parent__ = app_root.__name__ = None

        setattr(app_root, 'pycms_version', version)

        zodb_root['app_root'] = app_root

        import transaction
        transaction.commit()

    # create a globale images folder
    app_root = zodb_root['app_root']

    # Do necessary updates
    update(zodb_root['app_root'])

    initreq.registry.notify(AppRootReady(app_root, config.registry.settings))

    return zodb_root['app_root']


def root_factory(request):

    conn = get_connection(request)

    return conn.root()['app_root']


def main(global_config, **settings):

    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(root_factory=root_factory, settings=settings)
    zcml_file = settings.get('configure_zcml', 'configure.zcml')

    config.hook_zca()
    config.include(pyramid_zcml)
    config.include('pyramid_mailer')
    config.commit()

    config.scan('w20e.pycms')
    config.load_zcml(zcml_file)
    config.commit()

    appmaker(config)

    return config.make_wsgi_app()
