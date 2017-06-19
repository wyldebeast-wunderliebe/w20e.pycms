from repoze.catalog.catalog import Catalog as RepozeCatalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.indexes.path import CatalogPathIndex
from repoze.catalog.document import DocumentMap
from logging import getLogger
from w20e.hitman.utils import path_to_object, object_to_path
from .index import IIndexes


LOGGER = getLogger("w20e.pycms")


def init(event):

    """ Set up catalog for site. """

    app = event.app_root

    if event.registry.settings.get("pycms.catalog.force_new",
                                   False) or not hasattr(app, "_catalog"):
        app._catalog = Catalog()
        app._catalog.__parent__ = app
        app._catalog.__name__ = "catalog"
        app._catalog._p_changed = 1
        app._p_changed = 1

    indexes = event.registry.getUtility(IIndexes)

    for idx in indexes.get_indexes():
        if not idx[0] in list(app._catalog.catalog.keys()):
            if idx[1]['type'] == "field":
                app._catalog.catalog[idx[0]] = CatalogFieldIndex(
                    idx[1]['field'])
                app._catalog._p_changed = 1
            elif idx[1]['type'] == "text":
                app._catalog.catalog[idx[0]] = CatalogTextIndex(
                    idx[1]['field'])
                app._catalog._p_changed = 1
            elif idx[1]['type'] == "keyword":
                app._catalog.catalog[idx[0]] = CatalogKeywordIndex(
                    idx[1]['field'])
                app._catalog._p_changed = 1
            elif idx[1]['type'] == "path":
                app._catalog.catalog[idx[0]] = CatalogPathIndex(
                    idx[1]['field'])
                app._catalog._p_changed = 1


# event handlers
#
def objectRemoved(event):

    LOGGER.debug("Removing object %s" % event.object.id)

    cat = event.object.root._catalog
    cat.unindex_object(event.object)


def objectAdded(event):

    LOGGER.debug("Adding object %s" % event.object.id)

    cat = event.object.root._catalog
    cat.reindex_object(event.object)


def objectChanged(event):

    LOGGER.debug("Changed object %s" % event.object.id)

    cat = event.object.root._catalog

    try:
        cat.reindex_object(event.object)
    except:
        pass


class ObjectSummary(object):

    """ 'Brain'..."""

    def __init__(self, props={}):

        self.props = props

    def __getattr__(self, attrname):

        return self.props.get(attrname, '')

    @property
    def content_type(self):

        return self.ctype

    def __json__(self, request):
        """ return the properties for json rendering """
        return self.props


class Catalog(object):

    def __init__(self):

        self._catalog = RepozeCatalog()
        self._document_map = DocumentMap()

    @property
    def catalog(self):
        """ convenient proxy to real catalog """

        return self._catalog

    def query(self, qry, as_summary=False, as_object=False, **kwargs):

        """ Query the catalog. If as_summary is set, return object summaries,
        as fetched from info from the indexes"""

        res = self._catalog.query(qry, **kwargs)

        if as_summary:
            return [self.get_object_summary(uuid) for uuid in res[1]]
        elif as_object:
            return [self.get_object(uuid) for uuid in res[1]]
        else:
            return res

    def index_object(self, object):

        path = object_to_path(object)
        uuid = object.uuid

        docid = self._document_map.add(uuid)
        self._document_map.add_metadata(docid, {'path': path})

        try:
            self.catalog.index_doc(docid, object)
            self._p_changed = 1
            self.catalog._p_changed = 1
            self._document_map._p_changed = 1
            self.__parent__._p_changed = 1
        except:
            LOGGER.exception("Could not index object!")

    def reindex_object(self, object):

        uuid = object.uuid

        docid = self._document_map.docid_for_address(uuid)
        if not docid:
            self.index_object(object)
            docid = self._document_map.docid_for_address(uuid)

        # update the path of the object in the documentmap since the
        # object might have been renamed / moved
        path = object_to_path(object)
        self._document_map.add_metadata(docid, {'path': path})

        try:
            self.catalog.reindex_doc(docid, object)
            self._p_changed = 1
            self.catalog._p_changed = 1
            self._document_map._p_changed = 1
            self.__parent__._p_changed = 1
        except:
            LOGGER.exception("Could not index object!")

    def unindex_object(self, object):

        uuid = object.uuid

        docid = self._document_map.docid_for_address(uuid)
        if docid:
            self.catalog.unindex_doc(docid)
            self._document_map.remove_docid(docid)
            self._p_changed = 1
            self.catalog._p_changed = 1
            self._document_map._p_changed = 1
            self.__parent__._p_changed = 1

    def clear(self):

        self._catalog.clear()
        self._document_map = DocumentMap()
        self._p_changed = 1
        self.catalog._p_changed = 1
        self._document_map._p_changed = 1
        self.__parent__._p_changed = 1

    def get_object(self, docid):

        metadata = self._document_map.get_metadata(docid)
        path = metadata['path']
        return path_to_object(path, self.__parent__)

    def get_object_summary(self, uuid):

        """ Return a summary of the found object, based on the values that
        the indexes hold on the given uuid"""

        summ = {}

        for key in list(self.catalog.keys()):
            idx = self.catalog[key]
            if hasattr(idx, "_rev_index"):
                summ[key] = idx._rev_index.get(uuid, '')

        summ['key'] = uuid

        return ObjectSummary(summ)

    def list_objects(self):

        docids = self.list_object_ids()
        for docid in docids:
            metadata = self._document_map.get_metadata(docid)
            yield (docid, metadata['path'])

    def list_object_ids(self):

        return list(self._document_map.docid_to_address.keys())
