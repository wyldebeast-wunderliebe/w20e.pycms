import hashlib
from pyramid.threadlocal import get_current_registry
from zope.interface import Interface
from sharing import ISharing
from pyramid.security import Allow, DENY_ALL
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
import time
import random


KEY_LENGTH = 24


def init(event):

    """ Set up security for site. """

    app = event.app_root

    if not hasattr(app, 'acl'):

        setattr(app, 'acl', ACL(event.settings))


class ISecure(Interface):

    """ Marker """


class Secure:

    def __init__(self, context):

        self.context = context
        self.sharing = None

        try:
            self.sharing = get_current_registry().queryAdapter(context,
                                                               ISharing)
        except:
            pass

    @property
    def __acl__(self):

        return self.view_list() + self.edit_list() + [DENY_ALL]

    def edit_list(self):

        editors = [(Allow, 'group:admin', ('view', 'edit', 'admin'))]

        if self.sharing:
            for user_id in self.sharing.get_sharing().get('admin', []):
                editors.append((Allow, user_id, ('view', 'edit')))

        return editors

    def view_list(self):

        viewers = [(Allow, 'group:viewer', 'view')]

        if self.sharing:
            for user_id in self.sharing.get_sharing().get('viewer', []):
                viewers.append((Allow, user_id, 'view'))

        return viewers


class User(Persistent):

    """ Create user with given id. Profile may be empty, but may also
    be an object in the database. """

    def __init__(self, user_id, name, email, pwd,
                 profile=None, activation_key=None):

        self.id = user_id
        self.name = name
        self.email = email
        self.pwd = pwd and hashlib.sha224(pwd).hexdigest() or ''
        self.profile = profile

    def set_pwd(self, pwd):

        self.pwd = hashlib.sha224(pwd).hexdigest()

    def challenge(self, pwd):

        return self.pwd == hashlib.sha224(pwd).hexdigest()


class Group(Persistent):

    def __init__(self, group_id, users=None):

        if users is None:
            users = PersistentList()

        self.id = group_id
        self.users = users


class ACL(Persistent):

    """ Access control hub. The ACL can be instantiated and added to, say
    the root object, with attribute name acl. """

    def __init__(self, settings):

        self.users = PersistentMapping()
        self.groups = PersistentMapping()
        self.activation = PersistentMapping()

        admin, pwd = settings.get('pycms.admin_user',
                                  "admin:admin").split(":")

        self.users['admin'] = User(admin, "Administrator", "", pwd)
        self.groups['admin'] = Group('admin', users=PersistentList(['admin']))
        self.groups['viewers'] = Group('viewers')
        self.groups['editors'] = Group('editors')

    def generate_user_invite_key(self, user_id):

        """ Generate unique registration key for user and set on user. """

        if not user_id in self.users:
            return None

        t1 = time.time()
        time.sleep(random.random())
        t2 = time.time()
        base = hashlib.md5(str(t1 + t2))
        key = base.hexdigest()[:KEY_LENGTH]

        self.activation[key] = self.users[user_id]

        return key

    def get_user_for_activation(self, key):

        return self.activation.get(key, None)

    def unset_activation_key(self, key):

        if key in self.activation:
            del self.activation[key]

    def list_users(self):

        """ Return a dict of users, using the id as key """

        return self.users.keys()

    def list_groups(self):

        return self.groups.keys()

    def update_user(self, **data):

        self.users[data['email']].name = data['name']
        if data.get('pwd', None):
            self.users[data['email']].set_pwd(data['pwd'])

    def set_user_groups(self, user_id, groups=[]):

        """ Remove user from all groups, and then reset..."""

        for group_id in self.groups.keys():
            self.rm_user_from_group(group_id, user_id)

        for group_id in groups:
            self.add_user_to_group(group_id, user_id)

    def rm_user_from_group(self, group_id, user_id):

        if user_id in self.groups[group_id].users:
            idx = self.groups[group_id].users.index(user_id)
            del self.groups[group_id].users[idx]

    def add_user_to_group(self, group_id, user_id):

        if not user_id in self.groups[group_id].users:
            self.groups[group_id].users.append(user_id)

    def add_user(self, form, *args):

        """ form data input..."""

        self.create_user(**form.data.as_dict())

    def create_user(self, profile=None, **data):

        if data['email'] in self.users:
            return False

        self.users[data['email']] = User(data['email'], data['name'],
                                         data['email'], data.get('pwd', ''),
                                         profile=profile)

    def remove_user(self, user_id):

        if user_id in self.users:
            del self.users[user_id]
        # TODO clean up groups


def groupfinder(userid, request):

    user_groups = []

    if userid in request.root.acl.users.keys():
        for group in request.root.acl.groups.keys():
            if userid in request.root.acl.groups[group].users:
                user_groups.append("group:%s" % group)

    return user_groups
