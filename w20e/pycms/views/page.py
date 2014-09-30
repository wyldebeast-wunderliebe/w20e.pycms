from zope.interface import providedBy
from pyramid.security import has_permission
from pyramid.renderers import render_to_response
from base import ContentView, EditView
from w20e.pycms.models.image import Image
from w20e.pycms.layout.interfaces import ILayout, ILayouts


class LayoutView(object):

    """ Provide layout methods """

    @property
    def has_layout(self):

        return self.get_layout() is not None

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
            layout = [i for i in providedBy(self.context)
                      if i.extends(ILayout)][0]
        except:
            layout = self._default_layout

        layouts = self.request.registry.getUtility(ILayouts)

        return layouts.get_layout_by_if(layout)

    def get_blocks(self, slot_id):

        """ Return the blocks for the page """

        return self.context.get_blocks(slot_id)

    def render_slot(self, slot_id):

        """ Render the slot given by it's id """

        html = []

        for block in self.get_blocks(slot_id):

            html.append(block.render(self.request))

        return "\n".join(html)


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

    def __call__(self):

        context = super(PageView, self).__call__()
        context.update(
            {'view': self,
             'renderer_name': None,
             'renderer_info': None,
             'context': self.context,
             'request': self.request,
             'req': self.request,
             })

        return render_to_response(self.get_layout().template,
                                  context,
                                  request=self.request)


class PageEdit(EditView):

    pass


class PageLayout(EditView, LayoutView):

    pass


class ImageUpload(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        for key in self.request.params.keys():

            if getattr(self.request.params[key], "file", None):

                image_id = self.context._normalize_id(
                    self.request.params[key].filename)
                image_data = self.request.params[key].value

                image = Image(image_id,
                              {'name': image_id,
                               'data': {'name': image_id,
                                        'data': image_data}, })

                self.context.add_content(image)
