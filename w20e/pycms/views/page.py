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


class PageBlocks(PageView):

    """ Block view of page """

    @property
    def blocks(self):

        res = []

        for block in self.context.blocks:

            self._create_block_repr(block, res)

        return "".join(res)

    def _create_block_repr(self, block, data):

        data.append("""<div style="border: 1px solid red; padding: 5px">""")
        data.append("""<label>%s</label>""" % block.id)
        data.append("</div>")


class PageEdit(EditView):

    pass


class PageLayout(PageView):

    """ Edit view for page """

    @property
    def is_edit(self):

        return True

    @property
    def raw_content(self):

        return self.context._content

    def save(self):

        """ Parse html, and extract blocks. """

        parser = Parser(self.context)

        self.context.clear_blocks()

        parser.parse(self.request.params.get('content', ""))

        self.context._p_changed = True

        self.context._content = self.request.params.get('content', "")

        return {}

    def save_block(self):

        """ but not really... we only create the proper html """

        clazz = Registry.get_type(self.request.params.get('type'))

        if not clazz:
            return {'html': ''}

        block = clazz(self.request.params.get("id"), **self.request.params)

        if block['type'] == "image":

            if self.request.params.get('mode') == 'add':

                img_id = self.context.generate_content_id(
                        self.request.params.get('img').filename)

                img = Image(img_id,
                        {'name': img_id,
                         'data': {
                             'name': self.request.params.get('img').filename,
                             'data': self.request.params.get('img').value
                             }
                        })

                self.context.add_content(img)

                block['img_url'] = '%s%s' % (self.url, img_id)

                self.request.is_edit = True

                return "%s" % render_view(block, self.request)

        self.request.is_edit = True

        return render_view(block, self.request)

    def add_form(self):

        """ show add form for given type """

        typp = self.request.params.get('type')
        clazz = Registry.get_type(typp)

        if not clazz:
            return {'html': '<div class="message">No form found</div>'}

        tpl = PageTemplate(clazz.add_form)

        form = tpl(data={
            'id': generate_id(prefix="%s_" % typp, length=10)})

        return {'html': form}

    def edit_form(self):

        """ Show edit form for given block type """

        clazz = Registry.get_type(self.request.params.get('type'))

        if not clazz:
            return {'html': '<div class="message">No form found</div>'}

        tpl = PageTemplate(clazz.edit_form)

        data = self._params_to_dict(self.request.params)
        data['mode'] = 'edit'

        form = tpl(data=data)

        return {'html': form}

    def get_block(self, block_id):

        return self.context.get_block_by_ref(block_id)

    def page_actions(self):

        layoutsubs = [
            {'id': 'grid',
             'title': 'Grid',
             'action': 'javascript: pycms.selectLayout("grid")',
             'permission': 'edit'
             },
            {'id': '2col',
             'title': '2 columns',
             'action': 'javascript: pycms.selectLayout("2col")',
             'permission': 'edit'
             },
            {'id': '3col',
             'title': '3 columns',
             'action': 'javascript: pycms.selectLayout("3col")',
             'permission': 'edit'
             },
            {'id': '4col',
             'title': '4 columns',
             'action': 'javascript: pycms.selectLayout("4col")',
             'permission': 'edit'
             },                        
            ]

        subs = []

        for tp in Registry.list_types():

            subs.append({'id': 'add_%s' % tp,
                     'title': '%s' % tp,
                     'action': 'javascript: pycms.addBlock("%s")' % tp,
                     'permission': 'edit'
                     })

        return [
            {'id': 'pick_layout',
             'title': 'Select layout...',
             'action': '',
             'permission': 'edit',
             'subs': layoutsubs
             },
            {'id': 'add_block',
             'title': 'Add block...',
             'action': '',
             'permission': 'edit',
             'subs': subs
             },            
            {'id': 'delete',
             'title': 'Delete',
             'action': 'javascript: pycms.deleteBlock()',
             'permission': 'edit'
             },
            {'id': 'edit',
             'title': 'Edit',
             'action': 'javascript: pycms.editBlock()',
             'permission': 'edit'
             },
            {'id': 'cut',
             'title': 'Cut',
             'action': 'javascript: pycms.cutBlock()',
             'permission': 'edit'
             },
            {'id': 'paste',
             'title': 'Paste',
             'action': 'javascript: pycms.pasteBlock()',
             'permission': 'edit'
             },
            {'id': 'save',
             'title': 'Save',
             'action': 'javascript: pycms.savePage()',
             'permission': 'edit'
             },
            ]

    def _params_to_dict(self, params):

        """ create simple dict from multidict """

        simple = {}

        for key in params.keys():

            simple[key] = params.get(key)

        return simple
