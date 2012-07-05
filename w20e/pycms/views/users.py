from ..interfaces import IMailer
from pyramid.security import has_permission


class UserAdminView(object):

    """ User admin methods, all JSON """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def add_user(self):

        res = {'status': '', 'errors': ''}

        params = self.request.params

        if not (params.get('name') and params.get('email')):
            res.update({'status': 'error',
                        'errmsg': "not all required fields filled in"})
        elif params.get('pwd', None) != params.get('pwd_confirm', None):
            res.update({'status': 'error',
                        'errmsg': "passwords do not match"})
        else:
            user = self.context.root.acl.create_user(
                params['email'], pwd=params.get('pwd', None),
                name=params.get('name', None)
                )

            if user:
                res.update({'status': 'ok',
                            'user': {'name': user.name,
                                     'id': user.id,
                                     'email': user.email}
                            })
            else:
                res.update({'status': 'error',
                            'errmsg': 'User not created'
                            })
        return res

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

        res = {'status': '', 'token': '', 'errors': ''}

        user = None
        user_id = user_id or self.request.params.get('userid', None)
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
