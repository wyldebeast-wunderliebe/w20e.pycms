from base import AdminView
from w20e.forms.pyramid.formview import xmlformview
from w20e.forms.xml.formfile import FormFile, find_file
from ..interfaces import IMailer
from ..interfaces import ICatalogMapper
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer


class UserAddView(xmlformview):

    """ Add user form """

    def __init__(self, context, request):

        form = FormFile(find_file("../forms/user_add_form.xml",
                                  context.__class__))

        xmlformview.__init__(self, context, request, form, retrieve_data=True)


    def __call__(self):

        res = xmlformview.__call__(self)

        return self.renderform(errors=res['errors'])


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


    def set_password(self):

        user_id = self.request.params['user_id']

        key = self.context.acl.generate_user_invite_key(user_id)

        return self.change_password(token=key)


    def change_password(self, token=None):

        token = token or self.request.params['token']

        user = self.context.acl.get_user_for_activation(token)

        if not user:

            return {'status': 'error',
                    'macros': get_renderer('../templates/macros.pt').implementation(),
                    'main': get_renderer('../templates/main.pt').implementation(),
                    'token': '',
                    'message': 'No user found for this key!'}

        message = user.id

        if self.request.params.get('form.submitted', None):
            if self.request.params['password'] == self.request.params['password_confirm']:
                user.set_pwd(self.request.params['password'])
                self.context.acl.unset_activation_key(token)
                return HTTPFound(location = "login")
            else:
                message = "Passwords do not match"

        return {'status': 'ok', 'message': message, 'token': token,
                'macros': get_renderer('../templates/macros.pt').implementation(),
                'main': get_renderer('../templates/main.pt').implementation()

                }


    def pack_database(self):
        """ pack the database """

        db = self.db

        old_size = db.getSize()
        result = db.pack() or "Database has been packed succesfully"
        new_size = db.getSize()
        return "pack result: {0} \nOld Data.fs size: {1}\nNew Data.fs size: {2}\n"\
               "check disk to see size of blobdir".format(result, old_size, new_size)


    @property
    def db(self):

        from pyramid_zodbconn import get_connection
        conn = get_connection(self.request)
        db = conn.db()

        return db


    def catalog_entries(self):

        mapper = self.request.registry.getAdapter(self.context, ICatalogMapper)

        return [{'id': obj[0], 'path': obj[1]} for obj in mapper.list_objects()]


    def robots_txt(self):

        self.request.response.content_type = 'text/plain'

        return {}
