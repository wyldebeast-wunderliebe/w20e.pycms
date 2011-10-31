import hashlib
from pyramid.threadlocal import get_current_registry
from zope.interface import Interface
from sharing import ISharing
from pyramid.security import Allow, DENY_ALL
from persistent import Persistent
import time, random


KEY_LENGTH=24


class ISecure(Interface):

    """ Marker """


class Secure:

    def __init__(self, context):

        self.context = context
        self.sharing = None

        self.sharing = get_current_registry().queryAdapter(context, ISharing)


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

    def __init__(self, group_id, users=[]):

        self.id = group_id
        self.users = users


class ACL(Persistent):
    
    """ Access control hub. The ACL can be instantiated and added to, say
    the root object, with attribute name acl. """
    
    def __init__(self):

        self.users = {}
        self.groups = {}
        self.activation = {}

        reg = get_current_registry()

        admin, pwd = reg.settings.get('pycms.admin_user', "admin:admin").split(":")

        self.users['admin'] = User(admin, "Administrator", "", pwd)
        self.groups['admin'] = Group('admin', users=['admin'])
        self.groups['viewers'] = Group('viewers')
        self.groups['editors'] = Group('editors')


    def generate_user_invite_key(self, user_id):

        """ Generate unique registration key for user and set on user. """

        if not self.users.has_key(user_id):
            return None
        
        t1 = time.time()
        time.sleep( random.random() )
        t2 = time.time()
        base = hashlib.md5(str(t1 +t2) )
        key = base.hexdigest()[:KEY_LENGTH]

        self.activation[key] = self.users[user_id]

        return key


    def get_user_for_activation(self, key):

        return self.activation.get(key, None)


    def unset_activation_key(self, key):
        
        if self.activation.has_key(key):
            del self.activation[key]
            self._p_changed


    def list_users(self):

        """ Return a dict of users, using the id as key """

        return self.users.keys()

    
    def list_groups(self):

        return self.groups.keys()


    def update_user(self, **data):

        self.users[data['email']].name = data['name']
        if data.get('pwd', None):
            self.users[data['email']].set_pwd(data['pwd'])


    def create_user(self, profile=None, **data):

        self.users[data['email']] = User(data['email'], data['name'],
                                         data['email'], data.get('pwd', ''),
                                         profile=profile)

        self._p_changed = True

    def remove_user(self, user_id):

        if self.users.has_key(user_id):
            del self.users[user_id]
        # TODO clean up groups



def groupfinder(userid, request):

    user_groups = []
    
    if userid in request.root.acl.users.keys():
        for group in request.root.acl.groups.keys():
            if userid in request.root.acl.groups[group].users:
                user_groups.append("group:%s" % group)
                
    return user_groups
