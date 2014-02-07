import uuid
from zope.interface import providedBy
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from w20e.hitman.views.base import ContentView as Base
from w20e.hitman.views.base import DelView as DelBase
from w20e.hitman.views.base import EditView as EditBase
from w20e.hitman.views.base import BaseView as BaseBase
from w20e.hitman.models import Registry
from w20e.hitman.events import ContentAdded, ContentRemoved, ContentChanged
from w20e.hitman.utils import path_to_object

from pyramid.renderers import get_renderer, render
from pyramid.httpexceptions import HTTPFound
from pyramid.interfaces import IView, IViewClassifier
from pyramid.response import Response
from pyramid.security import authenticated_userid
from w20e.pycms.utils import has_permission
from pyramid.url import resource_url
from pyramid.compat import map_
from w20e.pycms.nature import INatures
from w20e.pycms.interfaces import IAdmin, ITemporaryObject
from w20e.pycms.events import TemporaryObjectCreated, TemporaryObjectFinalized

from ..actions import IActions
from ..ctypes import ICTypes
from ..macros import IMacros

from w20e.forms.pyramid.formview import formview as pyramidformview
from xml.dom.minidom import Document
from datetime import datetime
import copy


class ViewMixin(object):

    is_edit = False

    def add_macros(self, data):

        """ Add macros to rendering """

        if isinstance(data, dict):

            macros = self.request.registry.getUtility(IMacros)

            for macro in macros.list_macros():

                data[macro] = get_renderer(
                    macros.get_macro(macro)).implementation()

    @property
    def viewname(self):

        return self.request.path.split('/')[-1]

    @property
    def admin_title(self):

        """ title to be used in admin interface """

        reg = self.request.registry
        util = reg.getUtility(IAdmin)
        return util.title()

    @property
    def brand_title(self):

        """ brand title to be used in admin interface """

        reg = self.request.registry
        util = reg.getUtility(IAdmin)
        return util.brand_title()

    @property
    def keywords(self):

        try:
            return ",".join(
                (self.context.__data__['keywords'] or "").splitlines())
        except:
            return ""

    @property
    def description(self):

        try:
            return self.context.__data__['description'] or ''
        except:
            return ""

    @property
    def breadcrumbs(self):
        """ Find all parent objects to root """

        path = [self.context]
        _root = self.context

        while getattr(_root, "__parent__", None) is not None:
            _root = _root.__parent__
            path.append(_root)

        path.reverse()
        return path

    @property
    def perspectives(self):

        reg = self.request.registry

        actions = reg.getUtility(IActions)

        return [action for action in actions.get_actions("perspective",
                ctype=self.context.content_type) if (not action.permission) or
                has_permission(action.permission, self.context, self.request)]

    @property
    def siteactions(self):

        reg = self.request.registry

        util = reg.getUtility(IActions)

        actions = util.get_actions("site", ctype=self.context.content_type)

        return [action for action in actions
                if (not action.permission) or has_permission(action.permission,
                                                             self.context,
                                                             self.request)]

    @property
    def contentactions(self):

        reg = self.request.registry

        actions = reg.getUtility(IActions)

        return [action for action in actions.get_actions("content",
                ctype=self.context.content_type) if (not action.permission) or
                has_permission(action.permission, self.context, self.request)]

    @property
    def icon(self):
        ctypes = self.request.registry.getUtility(ICTypes)

        return ctypes.get_ctype_info(self.content_type).get("icon", "")

    def get_icon(self, ctype):
        ctypes = self.request.registry.getUtility(ICTypes)

        return ctypes.get_ctype_info(ctype).get("icon", "")

    @property
    def footer(self):
        return render('../templates/footer.pt', {})

    @property
    def base_url(self):

        return resource_url(self.context, self.request)

    def object_url(self, obj):

        """ return URL for the given object"""

        return resource_url(obj, self.request)

    @property
    def can_edit(self):

        return has_permission("edit", self.context, self.request)

    def user_has_permission(self, permission):

        return has_permission(permission, self.context, self.request)

    @property
    def user(self):

        return authenticated_userid(self.request) or ""

    @property
    def logged_in(self):

        return authenticated_userid(self.request) or None

    def render_viewlet(self, name, **kwargs):

        """ Render a viewlet """

        provides = [IViewClassifier] + map_(providedBy,
                                            (self.request, self.context))
        view = self.request.registry.adapters.lookup(
            provides, IView, name=name)

        self.request.update({'kwargs': kwargs})

        return "".join(view(self.context, self.request).app_iter)

    def has_nature(self, nature_id):

        natures = self.request.registry.getUtility(INatures)

        nature = natures.get_nature(nature_id)

        if nature:
            return self.context.has_nature(nature['interface'])
        else:
            return False


class BaseView(BaseBase, ViewMixin):

    def __call__(self):

        res = BaseBase.__call__(self)
        self.add_macros(res)

        return res


class ContentView(Base, ViewMixin):

    def __call__(self):

        res = Base.__call__(self)
        self.add_macros(res)

        return res

    def json(self):
        """ return a json encoded version of the context """

        return self.context


class AddView(BaseView):

    """ create temporary content """

    def __call__(self):

        ctype = self.request.params.get("ctype", None)

        clazz = Registry.get(ctype)

        initial_data = self.request.params.copy()
        del initial_data['ctype']

        content = clazz("_TMP", data=initial_data)

        content.owner = self.user

        content_id = str(uuid.uuid1())
        content.set_id(content_id)

        alsoProvides(content, ITemporaryObject)

        self.context.add_content(content)

        self.request.registry.notify(TemporaryObjectCreated(content))

        return HTTPFound(location='%sedit' %
                         self.request.resource_url(content))


class FactoryView(BaseView, pyramidformview, ViewMixin):
    """ add form for base content """

    is_edit = True

    def __init__(self, context, request):

        BaseView.__init__(self, context, request)

        self.context = context

        assert ITemporaryObject.providedBy(context), \
            "This object is not in a temporary state"

        self.form = self.context.__form__(request)
        pyramidformview.__init__(self, self.context, request, self.form,
                                 retrieve_data=True)

    #@property
    #def url(self):
    #    return "%s" % self.base_url

    @property
    def content_type(self):
        return self.context.content_type

    @property
    def after_add_redirect(self):

        url = self.request.registry.settings.get(
            'pycms.after_add_redirect', 'admin')

        if url[0] != "/":
            url = self.base_url + url

        return url

    @property
    def cancel_add_redirect(self):

        url = self.request.registry.settings.get(
            'pycms.cancel_add_redirect', 'admin')

        if url[0] != "/":
            parent_url = resource_url(self.context.__parent__, self.request)
            url = parent_url + url

        return url

    def __call__(self):

        errors = {}

        params = self.request.params

        submissions = set(["submit", "save", "w20e.forms.next",
                           "w20e.forms.process"])

        if submissions.intersection(params.keys()):
            status, errors = self.form.view.handle_form(self.form,
                                                        self.request.params)

        elif "cancel" in params:
            return HTTPFound(location=self.cancel_add_redirect)
        else:
            status = "unknown"

        # Hmm, looks like multipage. Store data and proceed...
        # even if there was a validation error, we still save the data
        # this will assure we store file inputs.
        self.form.submission.submit(self.form, self.context, self.request)

        if status == "completed":
            status = 'stored'
            parent = self.context.__parent__
            content_id = parent.generate_content_id(self.context.base_id)
            noLongerProvides(self.context, ITemporaryObject)
            self.request.registry.notify(
                TemporaryObjectFinalized(self.context))
            parent.rename_content(self.context.id, content_id)
            self.request.registry.notify(ContentAdded(self.context, parent))
            return HTTPFound(location=self.after_add_redirect)

        render_kwargs = {}

        render_args = {
            "form_class": "inline",
            "action": "{0}edit".format(self.base_url), }
        render_kwargs.update(render_args)

        rendered = self.form.view.render(
            self.form, errors=errors,
            status=status, data=self.request.params, context=self.context,
            **render_kwargs)
        rendered = rendered.decode('utf-8')
        res = {'status': status, 'errors': errors, 'rendered': rendered}

        self.add_macros(res)

        return res

    def ajax_submit_and_validate(self):

        redirect = None

        if "cancel" in self.request.params:
            redirect = self.cancel_add_redirect
        else:
            status, errors = self.form.view.handle_form(
                self.form, self.request.params)
            self.form.submission.submit(self.form, self.context, self.request)

            if status == "completed":
                # finalize the temporary object
                parent = self.context.__parent__
                content_id = parent.generate_content_id(self.context.base_id)
                noLongerProvides(self.context, ITemporaryObject)
                self.request.registry.notify(
                    TemporaryObjectFinalized(self.context))
                parent.rename_content(self.context.id, content_id)
                self.request.registry.notify(
                    ContentAdded(self.context, parent))
                redirect = self.after_add_redirect

        if redirect:
            doc = Document()
            root = doc.createElement("validation")
            doc.appendChild(root)
            command = doc.createElement("command")
            command.setAttribute("selector", "")
            command.setAttribute("name", 'redirect')
            command.setAttribute("value", "%s" % redirect)
            root.appendChild(command)
            results = doc.toprettyxml(indent="  ").encode('utf-8')
        else:
            results = pyramidformview.ajax_validate(self, "xml", True)

        return results


class EditView(EditBase, ViewMixin):

    is_edit = True

    @property
    def url(self):
        return "%sedit" % super(EditBase, self).url

    @property
    def after_edit_redirect(self):

        """ Where to go after successfull edit?"""

        url = self.request.registry.settings.get(
            'pycms.after_edit_redirect', 'edit')

        if url[0] != "/":
            url = self.base_url + url

        return url

    def __call__(self):

        res = EditBase.__call__(self)
        self.add_macros(res)

        return res

    def ajax_submit_and_validate(self):

        status, errors = self.form.view.handle_form(
            self.form, self.request.params)

        self.context._changed = datetime.now()

        self.form.submission.submit(self.form, self.context, self.request)

        results = pyramidformview.ajax_validate(self, "xml", True)

        self.request.registry.notify(ContentChanged(self.context))
        return results


class DelView(DelBase, ViewMixin):

    @property
    def url(self):
        return "%sadmin" % super(DelBase, self).url

    @property
    def after_del_redirect(self):

        url = self.request.registry.settings.get(
            'pycms.after_del_redirect', 'admin')

        if url[0] != "/":
            url = self.base_url + url

        return url

    @property
    def parent_url(self):
        return "%sadmin" % super(DelBase, self).parent_url

    def __call__(self):

        res = DelBase.__call__(self)
        self.add_macros(res)

        return res


class AdminView(Base, ViewMixin):

    is_edit = True

    def __call__(self):

        res = Base.__call__(self)
        self.add_macros(res)

        return res

    def remove_content(self, content_id=None):

        content_id = content_id or self.request.params.get('content_id', None)

        if content_id:

            content = self.context.get(content_id, None)

            self.context.remove_content(content_id)
            self.request.registry.notify(ContentRemoved(content, self))
            return True

        else:

            return False

    def order_content(self, order=None):

        order = order or self.request.params.get('order', None)

        if order:

            self.context.set_order(order.split(","))
            # reindex all subobjects, since position_in_parent has changed
            # TODO: can be done more efficient: only order has changed, so
            # perhaps a OrderChanged event.. and only reindex relevant index
            children = self.context.list_content()
            for child in children:
                self.request.registry.notify(ContentChanged(child))

            return True
        else:
            return False

    def paste_content(self):

        """ Ajax paste. This should recive a 'buffer' parameter """

        actions = self.request.params.get("buffer", "").split("::")
        result = {'status': 'ok'}
        mv = []
        cp = []

        for action in [a for a in actions if a]:
            try:
                title, path, action_id = action.split(";;")
                if action_id == "copy":
                    cp.append(path)
                else:
                    mv.append(path)
            except:
                result['status'] = "error"

        if mv:
            self.move_content(objs=mv)
        if cp:
            self.copy_content(objs=cp)

        return result

    def copy_content(self, objs=[]):
        """
        make a copy of the object and add it to current container
        if id already exists, create a copy-of id
        """
        copied = []

        objs = objs or self.request.params.get('objs', "").split("::")
        for path in objs:
            obj = path_to_object(path, self.context.root, path_sep=".")
            if obj is not None:
                cpy = copy.deepcopy(obj)
                # create new content id if it already exists
                cpy.set_id(self.context.generate_content_id(obj.id))
                self.context.add_content(cpy)
                self.request.registry.notify(ContentAdded(cpy, self.context))
                copied.append(cpy.id)

        return copied

    def move_content(self, objs=[]):

        """ Should receive a list of dotted paths """

        objs = objs or self.request.params.get('objs', "").split("::")

        moved = []

        for path in objs:

            obj = path_to_object(path, self.context.root, path_sep=".")

            if obj is not None:
                content = obj.__parent__.remove_content(obj.id)
                self.context.add_content(content)
                self.request.registry.notify(ContentChanged(content))
                moved.append(obj.id)

        return moved

    def rename_content(self, rename_map=None):

        """ Rename all content ids based on rename map"""

        rename = rename_map or self.request.params

        ret = {'status': 0, 'renamed': {}, 'errors': []}

        for id_from in rename.keys():

            if id_from == rename[id_from]:
                continue

            if id_from in self.context:

                id_to = rename[id_from]

                try:
                    self.context.rename_content(id_from, id_to)
                    ret['renamed'][id_from] = id_to
                    content = self.context.get(id_to, None)
                    self.request.registry.notify(ContentChanged(content))
                except:
                    ret['status'] = -1
                    ret['errors'].append("%s already exists" % id_to)
        return ret

    def list_content(self, **kwargs):

        """ If we're using the calalog, use the summary, otherwise do the
        usual"""

# TODO
# HUUB: I don't think this will work.. we need a path query, because the
# id is not unique within the application
#
#        if hasattr(self.context.root, "_catalog"):
#
#            cat = self.context.root._catalog
#            from repoze.catalog.query import Eq
#
#            summaries = []
#
#            for obj_id in self.context.list_content_ids():
#                uuid = cat.query(Eq("id", obj_id))[1][0]
#
#                summaries.append(cat.get_object_summary(uuid))
#
#            return summaries

        if False:
            pass
        else:
            return super(AdminView, self).list_content(**kwargs)

    def has_nature(self, nature_id):

        natures = self.request.registry.getUtility(INatures)

        nature = natures.get_nature(nature_id)

        if nature:
            return self.context.has_nature(nature['interface'])
        else:
            return False
