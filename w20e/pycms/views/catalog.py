from base import AdminView
from ..interfaces import ICatalog


class SiteCatalogView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)

    def catalog_entries(self):

        cat = self.request.registry.getAdapter(self.context, ICatalog)

        res = []

        for obj_uuid, path in cat.list_objects():

            obj = cat.get_object(obj_uuid)

            res.append({'id': obj.id,
                        'path': path,
                        'title': obj.title,
                        'ctype': obj.content_type})
        return res

    def catalog_indexes(self):

        cat = self.request.registry.getAdapter(self.context, ICatalog)

        res = []

        for item in cat.items():

            res.append({'id': item[0],
                        'docs': (hasattr(item[1], "_num_docs") and \
                                item[1]._num_docs() or -1),
                        'docids': item[1].docids()
                    })

        return res

    def reindex_catalog(self):

        reg = self.request.registry

        cat = reg.getAdapter(self.context, ICatalog)

        for path in cat.list_object_ids():
            cat.unindex_doc(path)

        cat.clear()

        cat.index_object(self.context)

        for obj in self.context.find_content():

            cat.index_object(obj)

        return self.__call__()
