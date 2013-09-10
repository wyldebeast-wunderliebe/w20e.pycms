from zope.interface import providedBy
from pyramid.view import render_view
from pyramid.security import has_permission
from pyramid.renderers import render_to_response
from chameleon import PageTemplate
from base import ContentView, EditView
from w20e.pycms.models.image import Image
from w20e.pycms.utils import generate_id
from w20e.pycms.layout.interfaces import ILayout, ILayouts


class LayoutView(object):

    """ Provide layout methods """

    @property
    def has_layout(self, layout=None):

        if not layout:
            return self.get_layout() is not None
        else:
            return self.get_layout() == layout

    @property
    def _default_layout(self):
        _layout = self.request.registry.settings.get(
            "pycms.default_layout", 
            "w20e.pycms.layout.interfaces.IBaseLayout")
        mod = __import__(".".join(_layout.split(".")[:-1]),
                         globals(), locals(), 
                         _layout.split(".")[-1], -1)

        return getattr(mod, _layout.split(".")[-1])
        
    def get_layout(self):

        """ A page can have one and only one layout. """
        
        try:
            layout = [i for i in providedBy(self.context) \
                          if i.extends(ILayout)][0]
        except:
            layout = self._default_layout

        layouts = self.request.registry.getUtility(ILayouts)

        return layouts.get_layout_by_if(layout)

    def get_blocks(self, slot_id):

        return self.context.get_blocks(slot_id)


class PageView(ContentView, LayoutView):

    """ Project specific view """

    def __init__(self, context, request):

        ContentView.__init__(self, context, request)

    @property
    def is_edit(self):

        return False

    @property
    def can_edit(self):

        return has_permission("edit", self.context, self.request)

    @property
    def content(self):

        """ We may or may not use a complex layout... """

        return self.context.__data__['text']

    def __call__(self):

        context = super(PageView, self).__call__()
        context.update(
            {'view':self,
             'renderer_name':None,
             'renderer_info':None,
             'context':self.context,
             'request':self.request,
             'req':self.request,
             })

        return render_to_response(self.get_layout().template,
                                  context,
                                  request=self.request)
        

class PageEdit(EditView):

    pass


class PageLayout(EditView, LayoutView):

    pass
