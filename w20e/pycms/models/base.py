import os
import inspect
from zope.interface import implements, directlyProvides, alsoProvides, \
     noLongerProvides, providedBy
from zope.component import subscribers
from zope.component import getMultiAdapter
from w20e.hitman.models.base import BaseFolder as HitmanBaseFolder
from w20e.hitman.models.base import BaseContent as HitmanBaseContent
from w20e.pycms.security import ISecure
from w20e.pycms.ctypes import ICTypes
from w20e.forms.interfaces import IFormFactory, IFormModifier
from w20e.forms.xml.factory import XMLFormFactory as BaseXMLFormFactory
from w20e.pycms.interfaces import INature


class XMLFormFactory(object):

    """ Base implementation of form factory. This guy tries to find
    xml forms in a directory called 'forms' in the app where the
    context lives, that are named after the content type of the given
    context object"""

    implements(IFormFactory)
    
    def __init__(self, context, request):

        self.context = context

    def createForm(self, form_name=None):

        form_path = os.path.join(
            os.path.dirname(inspect.getfile(self.context.__class__)), 
            "..", "forms", "%s.xml" % (form_name or self.context.content_type))

        xmlff = BaseXMLFormFactory(form_path)
        return xmlff.create_form(action="")


class SiteFormFactory(XMLFormFactory):

    """ Site uses page form """

    def createForm(self):

        return super(SiteFormFactory, self).createForm(form_name="page")


class PyCMSMixin:

    @property
    def __acl__(self):

        try:
            return ISecure(self).__acl__
        except:
            return []

    def __form__(self, request):

        """ Override for hitman form property, so as to enable
        form overrides and modifiers """

        try:
            return self._v_form
        except:
            factory = getMultiAdapter((self, request), IFormFactory)
            form = factory.createForm()

            for modifier in subscribers([self], IFormModifier):

                modifier.modify(form)

            self._v_form = form
            
            return self._v_form

    def add_nature(self, nature):

        alsoProvides(self, nature)

        del self._v_form

    def has_nature(self, nature):

        return nature in self.list_natures()

    def remove_nature(self, nature):

        noLongerProvides(self, nature)

        del self._v_form

    def set_natures(self, *natures):

        directlyProvides(self, *natures)

        del self._v_form

    def list_natures(self):

        return [i for i in providedBy(self) if i.extends(INature)]

    @property
    def natures(self):

        def to_str(iface):

            return "%s.%s" % (iface.__module__, iface.__name__)

        return [to_str(nature) for nature in self.list_natures()]


class BaseContent(PyCMSMixin, HitmanBaseContent):

    def allowed_content_types(self, request):
        return []


class BaseFolder(PyCMSMixin, HitmanBaseFolder):

    def allowed_content_types(self, request):

        ctypes = request.registry.getUtility(ICTypes)

        return ctypes.get_ctype_info(
            self.content_type).get("subtypes", "").split(",")
