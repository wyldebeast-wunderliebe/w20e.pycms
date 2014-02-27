import os
import inspect
import re
from datetime import datetime
from uuid import uuid1
from persistent.mapping import PersistentMapping
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from zope.interface import (
    implements, directlyProvides, alsoProvides, noLongerProvides, providedBy
)
from zope.component import subscribers
from zope.component import getMultiAdapter
from pyramid.url import resource_url
from w20e.forms.formdata import FormData
from w20e.pycms.utils import object_to_path
from w20e.pycms.security import ISecure
from w20e.forms.interfaces import IFormFactory, IFormModifier
from w20e.forms.xml.factory import XMLFormFactory as BaseXMLFormFactory
from w20e.pycms.interfaces import ITemporaryObject
from w20e.pycms.nature.interfaces import INature
from w20e.pycms.catalog import ObjectSummary
from interfaces import IContent, IFolder
from exceptions import UniqueConstraint
from copy import deepcopy


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


class Base(object):

    """ Base content, should be extended for real content """

    def __init__(self, content_id, data_attr_name="_DATA", data=None):

        # make sure mixin class __init__ methods get called as well
        super(Base, self).__init__(self, content_id, data_attr_name, data)

        if not data:
            data = {}

        # sanity check.. ID cannot be empty
        if not content_id:
            raise Exception("ID should not be empty")

        self._id = content_id
        self.data_attr_name = data_attr_name
        setattr(self, data_attr_name, OOBTree(data))
        self._created = datetime.now()
        self._changed = datetime.now()

    @property
    def id(self):

        return self._id

    def set_id(self, id):

        self._id = id

    @property
    def owner(self):
        """ get the creator userid """

        return getattr(self, '_owner', '')

    @owner.setter
    def owner(self, value):
        """ set the creator userid """

        self._owner = value
        self._p_changed = 1

    @property
    def content_type(self):

        return self.__class__.__name__.lower()

    @property
    def base_id(self):

        return self.content_type

    @property
    def has_parent(self):

        return getattr(self, "__parent__", None)

    @property
    def __data__(self):

        """ Wrap data in formdata container. Keep it volatile though,
        so as not to pollute the DB. """

        try:
            return self._v_data
        except:

            data = getattr(self, self.data_attr_name)

            # migrate old hashmaps to OOBTree if necessary
            if not isinstance(data, OOBTree):
                data = OOBTree(data)
                setattr(self, self.data_attr_name, data)

            self._v_data = FormData(data=data)
            return self._v_data

    def set_attribute(self, name, value):
        """ store an attribut in a low level manner """

        data = getattr(self, self.data_attr_name)
        data[name] = value
        self._changed = datetime.now()
        self._p_changed = 1
        # remove volatile cached data
        try:
            del(self._v_data)
        except:
            pass  # no worries.we didn't have the cached value

    @property
    def title(self):

        return self.id

    @property
    def created(self):

        return self._created

    @property
    def changed(self):

        return self._changed

    @property
    def root(self):

        _root = self

        while getattr(_root, "__parent__", None) is not None:
            _root = _root.__parent__

        return _root

    @classmethod
    def defaults(self):

        return {}

    @property
    def dottedpath(self):

        """ Return path as dot separated string """

        return object_to_path(self, path_sep=".", as_list=False)

    @property
    def __acl__(self):

        try:
            return ISecure(self).__acl__
        except:
            return []

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        # reset the uuid for the copied object
        delattr(result, '_uuid')
        return result

    @property
    def uuid(self):
        """ return a UUID, or generate it when not present yet """

        if not hasattr(self, '_uuid'):
            self._uuid = uuid1()
            self._p_changed = 1

        return str(self._uuid)

    def __hash__(self):
        """ return a hash of the uuid """
        return hash(self.uuid)

    def __eq__(self, other):
        """ check for equality based on the paths of the objects """

        if isinstance(other, self.__class__):
            return self.uuid == other.uuid
        else:
            return False

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

        """ form property that handles extra subscribers to the ctype """

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

        if hasattr(self, '_v_form'):
            del self._v_form

    def has_nature(self, nature):

        return nature in self.list_natures()

    def remove_nature(self, nature):

        noLongerProvides(self, nature)

        if hasattr(self, '_v_form'):
            del self._v_form

    def set_natures(self, *natures):

        directlyProvides(self, *natures)

        if hasattr(self, '_v_form'):
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


class BaseContent(Persistent, Base):

    """ Base content, should be extended for real content """

    implements(IContent)

    def __init__(self, content_id, data=None):

        if not data:
            data = {}

        Persistent.__init__(self)
        Base.__init__(self, content_id, data=data)

    def __repr__(self):
        """ return the ID as base representation """

        return self.id


class BaseFolder(PersistentMapping, Base):

    """ Base folder """

    implements(IFolder)

    def __init__(self, content_id, data=None):

        if not data:
            data = {}

        PersistentMapping.__init__(self)
        Base.__init__(self, content_id, data=data)
        self._order = []

    def __json__(self, request):
        """ return a json encoded version of this model
            including contained items
        """
        data = Base.__json__(self, request)
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

    def add_content(self, content):

        # don't replace the content
        if content.id in self:
            raise UniqueConstraint("an item with this ID already exists at \
                    this level")

        content.__parent__ = self
        content.__name__ = content.id
        self[content.id] = content
        self._order.append(content.id)

    def rename_content(self, id_from, id_to):

        """ Move object at id_from to id_to key"""

        if id_to in self:
            raise UniqueConstraint("an item with this ID already exists at \
                    this level")

        content = self.get(id_from, None)

        if content is None:
            return False

        del self[id_from]

        content._id = id_to
        content.__name__ = id_to

        # retain order
        if id_from in self._order:
            self._order[self._order.index(id_from)] = id_to

        self[content.id] = content

    def remove_content(self, content_id):

        try:
            content = self.get(content_id, None)
            del self[content_id]
            self._order.remove(content_id)
            return content
        except:
            return None

    def get_content(self, content_id, content_type=None):

        obj = self.get(content_id, None)

        if content_type:

            if getattr(obj, "content_type", None) == content_type:

                return obj

            else:

                return None

        return obj

    def _list_content_ids(self, **kwargs):
        """
        return all content IDs.
        NOTE: also returns temporary object IDs
        """

        all_ids = self.keys()

        def _order_cmp(a, b):

            max_order = len(self._order) + 1

            return cmp(self._order.index(a) if a in self._order
                       else max_order,
                       self._order.index(b) if b in self._order
                                               else max_order,
                       )

        all_ids.sort(_order_cmp)

        return all_ids

    def list_content(self, content_type=None, iface=None, **kwargs):

        """ List content of this folder. If content_type is given,
        list only these things.
        """

        all_content = []

        if content_type:
            if isinstance(content_type, str):
                content_type = [content_type]

            all_content = [
                obj for obj in self.values()
                if getattr(obj, 'content_type', None) in content_type]
        if iface:
            all_content = [
                obj for obj in self.values()
                if iface.providedBy(obj)]

        if not (content_type or iface):
            all_content = self.values()

        if kwargs.get('order_by', None):
            all_content.sort(lambda a, b:
                             cmp(getattr(a, kwargs['order_by'], 1),
                                 getattr(b, kwargs['order_by'], 1)))
        else:
            def _order_cmp(a, b):

                max_order = len(self._order) + 1

                return cmp(self._order.index(a.id) if a.id in self._order
                           else max_order,
                           self._order.index(b.id) if b.id in self._order
                           else max_order,
                           )

            all_content.sort(_order_cmp)

        # filter out temp objects
        return filter(
            lambda x: not ITemporaryObject.providedBy(x), all_content)

    def find_content(self, content_type=None):

        """ Find content recursively from the given folder. Use it
        wisely... """

        found = self.list_content(content_type=content_type)

        # recurse through folderish types.
        folders = self.list_content(iface=IFolder)

        for sub in folders:

            try:
                found += sub.find_content(content_type=content_type)
            except:
                # looks like it's not a folder...
                pass

        return found

    def _normalize_id(self, id):
        """ change all non-letters and non-numbers to dash """

        if isinstance(id, unicode):
            id = id.encode('utf-8')
        id = id.lower()
        id = re.sub('[^-a-z0-9_]+', '-', id)
        return id

    def generate_content_id(self, base_id):

        base_id = self._normalize_id(base_id)

        if not base_id in self:
            return base_id

        cnt = 1

        while "%s_%s" % (base_id, cnt) in self:
            cnt += 1

        return "%s_%s" % (base_id, cnt)

    def move_content(self, content_id, delta):

        """ Move the content in the order by delta, where delta may be
        negative """

        curr_idx = self._order.index(content_id)

        try:
            self._order.remove(content_id)
            self._order.insert(curr_idx + delta, content_id)
        except:
            pass

    def set_order(self, order=[]):

        self._order = order

    def __repr__(self):
        """ return the ID as base representation """

        return self.id
