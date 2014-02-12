from pyramid.response import FileResponse, Response
from base import BaseView, AdminView, ContentView
from w20e.forms.pyramid.formview import xmlformview as pyramidformview


class FormView(ContentView, pyramidformview):

    """ Form view """

    def __init__(self, context, request):

        ContentView.__init__(self, context, request)

        form = context.__data__['form']['data']

        pyramidformview.__init__(self, context, request, form)

    def __call__(self):

        res = ContentView.__call__(self)
        res.update(pyramidformview.__call__(self))

        return res

    @property
    def header(self):
        return self.context.__data__['header_text']

    @property
    def footer(self):
        return self.context.__data__['footer_text']


class FormAdminView(AdminView):

    def download_xml(self):

        value = self.context.__data__['form']

        response = Response(body=value['data'],
                            content_type="text/xml")

        # set response caching headers..
        response.cache_expires = (3600 * 24 * 7)

        return response
