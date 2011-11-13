from repoze.catalog.catalog import Catalog as RepozeCatalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex

from zope.interface import Interface
from pyramid.threadlocal import get_current_registry
from pyramid.traversal import find_resource
from pyramid.traversal import resource_path

from logging import getLogger
from interfaces import ICatalogMapper, ICatalog


LOGGER = getLogger("w20e.pycms")


# TODO: move mapping to DocumentMap of repoze.catalog

# event handlers
#
def objectRemoved(event):

    LOGGER.debug("Removing object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    #cat.unindex_doc(event.object.uuid)
    

def objectAdded(event):

    LOGGER.debug("Adding object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    mapper = reg.getAdapter(event.object.root, ICatalogMapper)

    uuid = mapper.gen_uuid()

    cat.index_doc(uuid, event.object)

    mapper.add_object(uuid, event.object)


def objectChanged(event):

    LOGGER.debug("Changed object %s" % event.object.id)

    reg = get_current_registry()
    cat = reg.getAdapter(event.object.root, ICatalog)
    #cat.reindex_doc(uuid, event.object)

    # TODO: lookup object uuid


class CatalogMapper(object):

    def __init__(self, site):

        self.site = site
        if not hasattr(self.site, "_catalog_map"):
            setattr(self.site, "_catalog_map", {})


    def clear(self):

        self.site._catalog_map.clear()
        self.site._p_changed = 1


    def gen_uuid(self):
        
        return max(self.site._catalog_map.keys() or [0]) + 1


    def add_object(self, uuid, obj):

        self.site._catalog_map[uuid] = resource_path(obj)
        self.site._p_changed = 1


    def get_object(self, uuid):

        path = self.site._catalog_map.get(uuid, None)

        if not path:
            return None

        return find_resource(self.site, path)

    
    def list_objects(self):

        return self.site._catalog_map.items()


    def list_object_ids(self):

        return self.site._catalog_map.keys()
        


class Catalog(object):

    def __init__(self, ctx):

        self.context = ctx

        if not hasattr(self.context, "_catalog"):
            self.context._catalog = RepozeCatalog()

        if not 'id' in self.context._catalog.keys():
            self.context._catalog['id'] = CatalogFieldIndex('id')

        if not 'title' in self.context._catalog.keys():
            self.context._catalog['title'] = CatalogFieldIndex('title')

        if not 'ctype' in self.context._catalog.keys():
            self.context._catalog['ctype'] = CatalogFieldIndex('content_type')

        if not 'text' in self.context._catalog.keys():
            self.context._catalog['text'] = CatalogTextIndex('full_text')

    def __getattr__(self, name):

        """ Proxy to real catalog """

        return getattr(self.context._catalog, name) 
