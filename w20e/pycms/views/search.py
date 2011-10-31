from base import BaseView
from ..interfaces import ICatalogMapper, ICatalog
from repoze.catalog.query import Contains
from pyramid.url import resource_url


class SearchView(BaseView):

    def __init__(self, context, request):

        BaseView.__init__(self, context, request)


    def __call__(self):

        """ Check text index on the given query. Assume simple query
        to start with... """

        qry = self.request.params.get('qry', '')

        if not qry:
            return {'found': 0, 'results': []}

        cat = self.request.registry.getAdapter(self.context.root, ICatalog)
        mapper = self.request.registry.getAdapter(self.context.root, ICatalogMapper)

        res = cat.query(Contains('text', qry))

        objs = []
        
        for result in res[1]:
            obj = mapper.get_object(result)
            objs.append({"title": obj.title, "href": resource_url(obj, self.request)})

        return {'found': res[0], 'results': objs}

            
