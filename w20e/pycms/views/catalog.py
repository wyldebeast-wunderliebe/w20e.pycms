from .base import AdminView
import paginate
from urllib.parse import urlencode


class SiteCatalogView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)
        self.cat = self.context.root._catalog

        params = request.params.copy()
        params.update({'page': '$page'})
        page_url = '{}?{}'.format(request.url, urlencode(params))
        # page_url = paginate.PageURL_WebOb(request)
        current_page = request.params.get('page', 0)
        self.entries = paginate.Page(
            self.catalog_entries(), current_page, url=page_url)

    def catalog_entries(self):

        res = []

        for docid, location in self.cat.list_objects():

            props = {'docid': docid, 'location': location}

            try:
                props.update(self.cat.get_object_summary(docid).props)

                res.append(props)
            except:
                pass
        return res

    def catalog_indexes(self):

        res = []

        for item in list(self.cat.catalog.items()):

            res.append({
                'id': item[0],
                'type': item[1].__class__.__name__,
                'docs': (hasattr(item[1], "_num_docs") and
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
