from repoze.catalog.catalog import Catalog as RepozeCatalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from pyramid.threadlocal import get_current_registry
from logging import getLogger
from interfaces import ICatalog
from w20e.hitman.utils import path_to_object, object_to_path
from BTrees.OOBTree import OOBTree


LOGGER = getLogger("w20e.pycms")


# TODO: move mapping to DocumentMap of repoze.catalog

# event handlers
#
def objectRemoved(event):

    LOGGER.debug("Removing object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    cat.unindex_object(event.object)


def objectAdded(event):

    LOGGER.debug("Adding object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    cat.index_object(event.object)


def objectChanged(event):

    LOGGER.debug("Changed object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    cat.unindex_object(event.object)


class Catalog(object):

    def __init__(self, site):

        self.site = site

        if not hasattr(self.site, "_catalog_uuid_to_path"):
            setattr(self.site, "_catalog_uuid_to_path", OOBTree())

        if not hasattr(self.site, "_catalog_path_to_uuid"):
            setattr(self.site, "_catalog_path_to_uuid", OOBTree())

        if not hasattr(self.site, "_catalog"):
            self.site._catalog = RepozeCatalog()

        if not 'id' in self.site._catalog.keys():
            self.site._catalog['id'] = CatalogFieldIndex('id')

        if not 'title' in self.site._catalog.keys():
            self.site._catalog['title'] = CatalogFieldIndex('title')

        if not 'ctype' in self.site._catalog.keys():
            self.site._catalog['ctype'] = CatalogFieldIndex('content_type')

        if not 'text' in self.site._catalog.keys():
            self.site._catalog['text'] = CatalogTextIndex('full_text')

    def __getattr__(self, name):

        """ Proxy to real catalog """

        return getattr(self.site._catalog, name)

    def gen_uuid(self):

        return max(self.uuid_to_path.keys() or [0]) + 1

    @property
    def catalog(self):
        """ convenient proxy to real catalog """

        return self.site._catalog

    @property
    def uuid_to_path(self):
        """ Get the uuid to path mapper """

        return self.site._catalog_uuid_to_path

    @property
    def path_to_uuid(self):
        """ Get the path to uuid mapper """

        return self.site._catalog_path_to_uuid

    def index_object(self, object):
        path = object_to_path(object)
        uuid = self.gen_uuid()
        self.catalog.index_doc(uuid, object)
        self.uuid_to_path[uuid] = path
        self.path_to_uuid[path] = uuid
        self._p_changed = 1

    def reindex_object(self, object):
        path = object_to_path(object)
        uuid = self.path_to_uuid[path]
        self.catalog.reindex_doc(uuid, object)

    def unindex_object(self, object):
        path = object_to_path(object)
        uuid = self.path_to_uuid[path]
        self.catalog.unindex_doc(uuid)

    def clear(self):

        self.site._catalog_uuid_to_path.clear()
        self.site._catalog_path_to_uuid.clear()
        self.site._p_changed = 1

    def get_object(self, uuid):

        path = self.uuid_to_path[uuid]
        return path_to_object(path, self.site)

    def list_objects(self):

        return self.uuid_to_path.items()

    def list_object_ids(self):

        return self.uuid_to_path.keys()
