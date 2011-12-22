from base import AdminView


class SiteCatalogView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)
        self.cat = self.context.root._catalog

    def catalog_entries(self):

        res = []

        for obj_uuid, path in self.cat.list_objects():

            obj = self.cat.get_object(obj_uuid)
            try:
                res.append({
                    'uuid': obj_uuid,
                    'id': obj.id,
                    'path': path,
                    'title': obj.title,
                    'ctype': obj.content_type})
            except:
                pass
        return res

    def catalog_indexes(self):

        res = []

        for item in self.cat.catalog.items():

            res.append({'id': item[0],
                        'type': item[1].__class__.__name__,
                        'docs': (hasattr(item[1], "_num_docs") and \
                                item[1]._num_docs() or 0),
                        'docids': item[1].docids()
                    })

        return res

    def reindex_catalog(self):

        self.cat.clear()

        self.cat.index_object(self.context)

        for obj in self.context.find_content():

            self.cat.index_object(obj)

        return self.__call__()
