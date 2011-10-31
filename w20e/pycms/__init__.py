from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
import pyramid_zcml
from models.site import Site
from models.imagefolder import ImageFolder
from paste.script import command
from pyramid.paster import get_app
from ZODB.FileStorage.FileStorage import FileStorage
from ZODB.blob import BlobStorage

# Register pyramidfile
from w20e.forms.registry import Registry
from w20e.forms.pyramid.file import PyramidFile

Registry.register_renderable("file", PyramidFile)



def update(app):

    """ Any updates can go here... """

    if hasattr(app, 'list_content') and not hasattr(app, "_order"):

        setattr(app, "_order", [])

        for thing in app.values():

            update(thing)



def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Site("welcome")
        app_root.__data__['name'] = 'welcome'
        app_root.__parent__ = app_root.__name__ = None

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

    return zodb_root['app_root']


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


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
    return config.make_wsgi_app()
