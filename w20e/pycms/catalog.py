from repoze.catalog.catalog import Catalog as RepozeCatalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from logging import getLogger
from w20e.hitman.utils import path_to_object, object_to_path
from BTrees.OOBTree import OOBTree
from index import IIndexes


LOGGER = getLogger("w20e.pycms")


def init(event):

    """ Set up catalog for site. """

    app = event.app_root

    if event.registry.settings.get("pycms.catalog.force_new", False) \
           or not hasattr(app, "_catalog"):
        app._catalog = Catalog()
        app._catalog.__parent__ = app
        app._catalog.__name__ = "catalog"
        app._p_changed

    indexes = event.registry.getUtility(IIndexes)

    for idx in indexes.get_indexes():
        if not idx[0] in app._catalog.catalog.keys():
            if idx[1]['type'] == "field":
                app._catalog.catalog[idx[0]] = \
                                             CatalogFieldIndex(idx[1]['field'])
            elif idx[1]['type'] == "text":
                app._catalog.catalog[idx[0]] = \
                                             CatalogTextIndex(idx[1]['field'])


# event handlers
#
def objectRemoved(event):

    LOGGER.debug("Removing object %s" % event.object.id)

    cat = event.object.root._catalog
    cat.unindex_object(event.object)


def objectAdded(event):

    LOGGER.debug("Adding object %s" % event.object.id)

    cat = event.object.root._catalog
    cat.index_object(event.object)


def objectChanged(event):

    LOGGER.debug("Changed object %s" % event.object.id)

    cat = event.object.root._catalog

    try:
        cat.reindex_object(event.object)
    except:
        pass


class Catalog(object):

    def __init__(self):

        self._catalog = RepozeCatalog()
        self.uuid_to_path = OOBTree()
        self.path_to_uuid = OOBTree()

    def gen_uuid(self):

        return max(self.uuid_to_path.keys() or [0]) + 1

    @property
    def catalog(self):
        """ convenient proxy to real catalog """

        return self._catalog

    def query(self, *args, **kwargs):

        return self._catalog.query(*args, **kwargs)

    def index_object(self, object):

        path = object_to_path(object)
        uuid = self.gen_uuid()
        self.catalog.index_doc(uuid, object)
        self.uuid_to_path[uuid] = path
        self.path_to_uuid[path] = uuid
        self.__parent__._p_changed = 1

    def reindex_object(self, object):

        path = object_to_path(object)
        uuid = self.path_to_uuid.get(path, None)

        if uuid:
            self.catalog.reindex_doc(uuid, object)
        else:
            self.index_object(object)
        self.__parent__._p_changed = 1

    def unindex_object(self, object):

        path = object_to_path(object)
        uuid = self.path_to_uuid[path]
        self.catalog.unindex_doc(uuid)
        del self.uuid_to_path[uuid]
        del self.path_to_uuid[path]
        self.__parent__._p_changed = 1

    def clear(self):

        self._catalog.clear()
        self.uuid_to_path.clear()
        self.path_to_uuid.clear()
        self.__parent__._p_changed = 1

    def get_object(self, uuid):

        path = self.uuid_to_path[uuid]
        return path_to_object(path, self.__parent__)

    def list_objects(self):

        return self.uuid_to_path.items()

    def list_object_ids(self):

        return self.uuid_to_path.keys()
