import hashlib
from pyramid.threadlocal import get_current_registry
from zope.interface import Interface, Attribute, implements
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

    if event.registry.settings.get("pycms.acl.force_new", False) \
           or not hasattr(app, "acl"):

        setattr(app, 'acl', ACL(event.registry.settings))
        app.acl.__parent__ = app
        app.acl.__name__ = "ACL"
        app._p_changed = 1

    # ALWAYS reset admin pwd...
    admin, pwd = event.registry.settings.get('pycms.admin_user',
                                             "admin:admin").split(":")

    app.acl.users['admin'] = User(admin, "Administrator", "", pwd)


class IACLRequest(Interface):

    acl = Attribute("The ACL list")
    context = Attribute("The context of which the ACL is requested")


class ACLRequest(object):

    implements(IACLRequest)

    def __init__(self, acl, context):

        self.acl = acl
        self.context = context
        

class ISecure(Interface):

    """ Marker """


class Secure:

    def __init__(self, context):

        self.context = context

    @property
    def __acl__(self):

        acl = self.viewers() + self.editors() + [DENY_ALL]

        get_current_registry().notify(ACLRequest(acl, self.context))

        return acl

    def editors(self):

        return [(Allow, 'group:admin', ('view', 'edit', 'admin'))]

    def viewers(self):

        return [(Allow, 'group:viewer', 'view')]


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

    def create_user(self, email, pwd=None, name='', profile=None):

        if email in self.users:
            return None

        self.users[email] = User(email, name or email,
                                 email, pwd,
                                 profile=profile)

        return self.users[email]

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
