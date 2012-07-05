from w20e.hitman.views.base import ContentView as Base
from w20e.hitman.views.base import AddView as AddBase
from w20e.hitman.views.base import DelView as DelBase
from w20e.hitman.views.base import EditView as EditBase
from w20e.hitman.views.base import BaseView as BaseBase
from w20e.hitman.events import ContentRemoved
from w20e.hitman.utils import path_to_object

from pyramid.renderers import get_renderer, render
from pyramid.security import authenticated_userid
from w20e.pycms.utils import has_permission
from pyramid.url import resource_url

from ..actions import IActions
from ..ctypes import ICTypes
from ..macros import IMacros


def add_macros(data, view):

    """ Add macros to rendering """

    if type(data) == type({}):

        macros = view.request.registry.getUtility(IMacros)

        for macro in macros.list_macros():

            data[macro] = get_renderer(
                macros.get_macro(macro)).implementation()


class ViewMixin:

    is_edit = False

    @property
    def viewname(self):

        return self.request.path.split('/')[-1]

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


class BaseView(BaseBase, ViewMixin):

    def __call__(self):

        res = BaseBase.__call__(self)
        add_macros(res, self)

        return res


class ContentView(Base, ViewMixin):

    def __call__(self):

        res = Base.__call__(self)
        add_macros(res, self)

        return res


class AddView(AddBase, ViewMixin):

    is_edit = True

    @property
    def url(self):

        return "%sadmin" % self.base_url

    @property
    def after_add_redirect(self):
        return "%s%s" % (self.base_url,
                self.request.registry.settings.get('pycms.after_add_redirect',
                    'admin'))

    @property
    def cancel_add_redirect(self):
        return "%s%s" % (self.base_url, self.request.registry.settings.get(
            'pycms.cancel_add_redirect', 'admin'))

    def __call__(self):

        res = AddBase.__call__(self)
        add_macros(res, self)

        return res


class EditView(EditBase, ViewMixin):

    is_edit = True

    @property
    def url(self):
        return "%sedit" % super(EditBase, self).url

    @property
    def after_edit_redirect(self):

        """ Where to go after successfull edit?"""

        return "%s%s" % (self.base_url, self.request.registry.settings.get(
            'pycms.after_edit_redirect', 'edit'))

    def __call__(self):

        res = EditBase.__call__(self)
        add_macros(res, self)

        return res


class DelView(DelBase, ViewMixin):

    @property
    def url(self):
        return "%sadmin" % super(DelBase, self).url

    @property
    def after_del_redirect(self):

        """ Where to go after successfull edit?"""

        return "%s%s" % (self.base_url, self.request.registry.settings.get(
            'pycms.after_del_redirect', 'admin'))

    @property
    def parent_url(self):
        return "%sadmin" % super(DelBase, self).parent_url

    def __call__(self):

        res = DelBase.__call__(self)
        add_macros(res, self)

        return res


class AdminView(Base, ViewMixin):

    is_edit = True

    def __call__(self):

        res = Base.__call__(self)
        add_macros(res, self)

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
            return True
        else:
            return False

    def paste_content(self):

        """ Ajax paste. This should recive a 'buffer' parameter """

        actions = self.request.params.get("buffer", "").split("::")
        result = {'status': 'ok'}
        mv = []

        for action in actions:
            try:
                title, path, action_id = action.split(";;")
                if action_id == "copy":
                    pass
                else:
                    mv.append(path)
            except:
                result['status'] = "error"

        self.move_content(objs=mv)

        return result

    def move_content(self, objs=[]):

        """ Should receive a list of dotted paths """

        objs = objs or self.request.params.get('objs', "").split("::")

        moved = []

        for path in objs:

            obj = path_to_object(path, self.context.root, path_sep=".")

            if obj is not None:
                content = obj.__parent__.remove_content(obj.id)
                self.context.add_content(content)
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
