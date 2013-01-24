import os
import inspect
from uuid import uuid1
from zope.interface import implements, directlyProvides, alsoProvides, \
     noLongerProvides, providedBy
from zope.component import subscribers
from zope.component import getMultiAdapter
from pyramid.url import resource_url
from w20e.hitman.models.base import BaseFolder as HitmanBaseFolder
from w20e.hitman.models.base import BaseContent as HitmanBaseContent
from w20e.hitman.utils import object_to_path
from w20e.pycms.security import ISecure
from w20e.pycms.ctypes import ICTypes
from w20e.forms.interfaces import IFormFactory, IFormModifier
from w20e.forms.xml.factory import XMLFormFactory as BaseXMLFormFactory
from w20e.pycms.interfaces import INature, ITemporaryObject
from w20e.pycms.models.interfaces import IPyCMSMixin
from w20e.pycms.catalog import ObjectSummary


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


class PyCMSMixin(object):

    implements(IPyCMSMixin)

    @property
    def __acl__(self):

        try:
            return ISecure(self).__acl__
        except:
            return []

    @property
    def uuid(self):
        """ return a UUID, or generate it when not present yet """

        if not hasattr(self, '_uuid'):
            self._uuid = uuid1()
            self._p_changed = 1

        return str(self._uuid)

    @property
    def path(self):
        """ return the path of this resource """

        return object_to_path(self)

    @property
    def position_in_parent(self):
        """ return the position of this object in the parent container """
        parent = self.__parent__
        return parent and parent._order.index(self.id) or 0

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


    def __json__(self, request):
        """ return a json encoded version of this model """

        # use the form data as default
        data = self.__data__.as_dict()

        # add content item's properties that are not part of the form..
        data['id'] = self.id
        data['uid'] = self.uuid
        data['content_type'] = self.content_type
        data['changed'] = self.changed.isoformat()
        data['created'] = self.created.isoformat()
        data['owner'] = self.owner
        data['path'] = self.path
        data['position_in_parent'] = self.position_in_parent
        data['url'] = resource_url(self, request)

        return data


class BaseContent(PyCMSMixin, HitmanBaseContent):

    def allowed_content_types(self, request):
        return []


class BaseFolder(PyCMSMixin, HitmanBaseFolder):

    def __json__(self, request):
        """ return a json encoded version of this model 
            including contained items
        """
        data = PyCMSMixin.__json__(self, request)
        items = self.list_content()
        contained_items = []

        for item in items:

            # candidate for refactoring.. some kind of generic 'brain' needed
            attributes = ['uuid', 'id', 'title', 'content_type']
            props = {'ctype': item.content_type}
            for a in attributes:
                props[a] = getattr(item, a, None)
            brain = ObjectSummary(props)
            contained_items.append(brain)

        data['contained_items'] = contained_items
        return data

    def list_content(self, content_type=None, iface=None, **kwargs):
        """ use base listing, but filter out temp objects """

        result = HitmanBaseFolder.list_content(
                self, content_type, iface, **kwargs)

        # filter out temp objects
        result = [r for r in result if not ITemporaryObject.providedBy(r)]
        return result

    def allowed_content_types(self, request):

        ctypes = request.registry.getUtility(ICTypes)

        return ctypes.get_ctype_info(
            self.content_type).get("subtypes", "").split(",")
