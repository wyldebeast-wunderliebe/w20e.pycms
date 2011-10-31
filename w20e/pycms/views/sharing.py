from base import AdminView
from pyramid.httpexceptions import HTTPFound
from ..sharing import ISharing


class SharingView(AdminView):

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)
        self.sharing = request.registry.getAdapter(self.context, ISharing)


    def list_user_ids(self):
        
        return self.context.root.acl.list_users()


    def list_group_ids(self):

        return self.context.root.acl.list_groups()


    def __call__(self):

        res = AdminView.__call__(self)

        if self.request.params.get("submit", None) == "save":

            _sharing = {}

            for user_id in self.list_user_ids():

                for group_id in self.list_group_ids():

                    if self.request.params.get("map--%s--%s" % (group_id, user_id), None):
                        if not _sharing.has_key(group_id):
                            _sharing[group_id] = []

                        _sharing[group_id].append(user_id)

            self.sharing.set_sharing(_sharing)

        elif self.request.params.get("submit", None) == "cancel":

            return HTTPFound(location=self.url)

        return res


    def get_sharing(self):

        return self.sharing.get_sharing()


    def inherited(self, user_id, group_id):

        return user_id in self.context.root.acl.groups[group_id].users


    def is_shared(self, group_id, user_id):

        return user_id in self.sharing.get_sharing().get(group_id, [])
