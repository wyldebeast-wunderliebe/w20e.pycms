import inspect
import os
from persistent.mapping import PersistentMapping
from zope.component import getMultiAdapter
from zope.interface import implements
from pyramid.view import render_view
from w20e.forms.pyramid.formview import formview as pyramidformview
from w20e.forms.xml.factory import XMLFormFactory as BaseXMLFormFactory
from w20e.forms.interfaces import IFormFactory
from w20e.pycms.layout.interfaces import ILayouts
from interfaces import IBlock


class XMLFormFactory(object):

    """ Base implementation of form factory. This guy tries to find
    xml forms in the directory where the context lives, that are named
    after the content type of the given context object"""

    implements(IFormFactory)

    def __init__(self, context, request):

        self.context = context

    def createForm(self, action, form_name=None):

        form_path = os.path.join(
            os.path.dirname(inspect.getfile(self.context.__class__)),
            "%s.xml" % (form_name or self.context.type))

        xmlff = BaseXMLFormFactory(form_path)
        form = xmlff.create_form(action=action)

        form.data.from_dict(self.context)

        return form


class Block(PersistentMapping):

    implements(IBlock)

    def __init__(self, block_id, **props):

        super(Block, self).__init__()
        self.id = block_id
        self.update(props)

    def __repr__(self):

        return "%s; %s" % (self.type, self.items())

    @property
    def type(self):

        return self.__class__.__name__.lower()


class BlockView(object):

    """ Base view for blocks """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        return {}

    @property
    def type(self):

        return self.context.type

    @property
    def id(self):

        return self.context['id']


class BlockEdit(pyramidformview, BlockView):

    """ Base edit view for blocks """

    def __init__(self, context, request, form=None):

        self.context = context
        self.request = request

        pyramidformview.__init__(self, context, request,
                self.__form__(request))
        BlockView.__init__(self, context, request)

    @property
    def action(self):

        return self.request.url

    def _get_block(self):

        if "slot" in self.request.params.keys() and \
                "block" in self.request.params.keys():
            return self.context.get_block(self.request.params["slot"],
                                          self.request.params["block"])
        else:
            layouts = self.request.registry.getUtility(ILayouts)

            factory = layouts.get_block(self.request.params["type"])

            return factory("TMP")

    def __form__(self, request):

        try:
            return self._v_form
        except:

            block = self._get_block();

            factory = getMultiAdapter((block, request), IFormFactory)
            form = factory.createForm(request.url)

            self._v_form = form

            return self._v_form

    def __call__(self):
        
        result = super(BlockEdit, self).__call__()

        if result['errors']:
            self.request.response.status = 202
        elif result['status'] in ["processed", "stored"]:

            # TODO: store temporary block. Only on page save is this
            # info actually stored
            layouts = self.request.registry.getUtility(ILayouts)

            factory = layouts.get_block(self.request.params["type"])

            data = self.form.data.as_dict()

            block = factory(self.form.data['name'], tmp=True, **data)

            self.context.save_block(self.request.params["slot"], 
                                    block.id, block)

        return result


BlockAdd = BlockEdit
