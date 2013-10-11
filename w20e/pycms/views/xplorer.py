from pyramid.url import resource_url
from w20e.pycms.ctypes import ICTypes


class XPlorerView(object):
    
    """ Object explorer """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        return {}

    def list_content(self):

        """ List all children """

        return self.context.list_content()

    @property
    def has_parent(self):

        """ Is there something above? """

        return self.context.has_parent

    @property
    def xplore_parent_url(self):

        if self.has_parent:

            return "%sxplore" % resource_url(
                self.context.__parent__, self.request)
        else:
            return "#"
        
    def xplore_url(self, obj):

        return "%sxplore" % resource_url(obj, self.request)

    def get_icon(self, ctype):

        ctypes = self.request.registry.getUtility(ICTypes)

        return ctypes.get_ctype_info(ctype).get("icon", "")
