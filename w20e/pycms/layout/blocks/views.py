import inspect
import os
import uuid
from zope.component import getMultiAdapter
from zope.interface import implements
from pyramid.httpexceptions import HTTPFound
from w20e.forms.pyramid.formview import formview as pyramidformview
from w20e.forms.xml.factory import XMLFormFactory as BaseXMLFormFactory
from w20e.forms.interfaces import IFormFactory
from w20e.forms.form import FormValidationError
from w20e.pycms.layout.interfaces import ILayouts


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

            block = self._get_block()

            factory = getMultiAdapter((block, request), IFormFactory)
            form = factory.createForm(request.url)

            self._v_form = form

            return self._v_form

    def _gen_block_id(self):

        return str(uuid.uuid1())[:8]

    def __call__(self):

        result = {'status': "", 'errors': ""}

        if self.request.method == "POST":

            (result['status'], result['errors']) = self.handle_form()

            if result['errors']:
                self.request.response.status = 202
            else:
                block = self._get_block()

                self.form.submission.submit(self.form, block, self.request)

                if block.id == "TMP":
                    block.id = self._gen_block_id()
                    self.context.save_block(self.request.params["slot"],
                                            block.id, block)
                else:
                    block._p_changed

                result = HTTPFound(location='block?block=%s&slot=%s' %
                                   (block.id, self.request.params["slot"]))

        return result

    def handle_form(self):

        """ Handle the form. Override this method if you wish... """

        form = self.form
        self._process_data(form, form.view, self.request.params)
        status = 'processed'
        errors = {}

        try:
            form.validate()
            status = 'stored'

        except FormValidationError, fve:
            errors = fve.errors
            status = 'error'

        return (status, errors)


BlockAdd = BlockEdit


class BlockRemove(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        self.context.rm_block(self.request.params['slot'],
                              self.request.params['block'])

        return {"status": 0, "msg": "Block removed"}


class BlockView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        block = self.context.get_block(self.request.params['slot'],
                                       self.request.params['block'])

        return {"block": block, "slot": self.request.params['slot']}
