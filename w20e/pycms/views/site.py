from base import AdminView
from ..interfaces import IMailer
from pyramid.security import has_permission


class SiteView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)

    def list_users(self):

        return self.context.acl.users.values()

    def list_groups(self):

        return self.context.acl.groups.values()

    def list_activation(self):

        acts = []

        for key in self.context.acl.activation.keys():
            user = self.context.acl.get_user_for_activation(key)

            acts.append((user.id, key))

        return acts

    def delete_user(self):

        """ Remove user with give id from acl """

        user_id = self.request.params['user_id']

        self.context.acl.remove_user(user_id)

        return "OK"

    def invite_user(self):

        user_id = self.request.params['user_id']

        mailer = self.request.registry.getUtility(IMailer)

        key = self.context.acl.generate_user_invite_key(user_id)

        mailer.invite_user(self.request, user_id, key)

    def user_groups(self):

        """ admin user groups """

        if self.request.params.get("group", []):
            self.context.acl.set_user_groups(
                self.request.params['user'],
                self.request.params.getall('group'),
                )

        return {'groups': self.context.acl.groups.values(),
                'user': self.request.params.get('user_id', '')}

    def delete_key(self):

        self.context.acl.unset_activation_key(
                self.request.params.get('key', ''))

    def change_password(self, token=None, user_id=None):

        """ Change password given the token."""

        res = super(SiteView, self).__call__()
        res.update({'status': '', 'token': '', 'errors': ''})
        user = None

        user_id = user_id or self.request.params.get('user_id', None)
        token = token or self.request.params.get('token', None)

        res.update({'user_id': user_id, 'token': token})

        if self.request.method != "POST":
            return res

        # we could be admin...
        if not token:
            if user_id and has_permission("admin", self.context, self.request):
                user = self.context.acl.users[user_id]
        else:
            user = self.context.acl.get_user_for_activation(token)

        if not user:

            res.update({'status': 'error',
                        'errors': 'No user found for this key!'})
            return res

        message = user.id
        status = 'ok'

        if not self.request.params.get('password', None):
            message = "Cannot be empty"
            status = "error"
        elif self.request.params['password'] == \
               self.request.params['password_confirm']:
            user.set_pwd(self.request.params['password'])
            if token:
                self.context.acl.unset_activation_key(token)
            message = "Password reset"
        else:
            message = "Passwords do not match"
            status = 'error'

        res.update({'status': status, 'errors': message,
                    'token': token})
        return res

    def pack_database(self):
        """ pack the database """

        db = self.db

        old_size = db.getSize()
        result = db.pack() or "Database has been packed succesfully"
        new_size = db.getSize()
        return "pack result: {0} \nOld Data.fs size: {1}\n" \
                "New Data.fs size: {2}\n" \
                "check disk to see size of blobdir".format(
                        result, old_size, new_size)

    @property
    def db(self):

        from pyramid_zodbconn import get_connection
        conn = get_connection(self.request)
        db = conn.db()

        return db

    def catalog_entries(self):

        return [{'id': obj[0], 'path': obj[1]} for obj in \
                self.context._catalog.list_objects()]

    def robots_txt(self):

        self.request.response.content_type = 'text/plain'

        return {}
