from pyramid.security import has_permission

from base import ContentView, EditView
from ..models.image import Image
from ..parser import Parser
from pyramid.view import render_view
from ..blocks.registry import Registry
from ..utils import generate_id

from chameleon import PageTemplate


class PageView(ContentView):

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

        if not self.context.__data__['use_complex_layout']:

            return self.context.__data__['text']

        html = []

        self.request.is_edit = self.is_edit

        height = 0

        for block in self.context.blocks:

            try:
                block_height = int(float(block.get("height", "200px")[:-2]))
                block_top = int(float(block.get("top", "10px")[:-2]))

                height = max(height, block_top + block_height)
            except:
                pass

            html.append(render_view(block, self.request))

        return """<div class="content" style="min-height: %spx">%s</div>""" \
                % (height + 20, "".join(html))

    @property
    def layout(self):

        html = []

        self.request.is_edit = self.is_edit

        for block in self.context.blocks:

            html.append(render_view(block, self.request))

        return "".join(html)


class PageEdit(EditView):

    pass


class PageLayout(PageView):

    """ Edit view for page """

    @property
    def is_edit(self):

        return True

    @property
    def has_layout(self):

        return self.context.layout
