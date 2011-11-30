from pyramid.security import Allow
from zope.interface import Interface


SHARING_ATTR = "_sharing"


class ISharing(Interface):

    """ Marker for sharing """


class Sharing(object):

    def __init__(self, context):

        self.context = context

    def set_sharing(self, sharing={}):

        setattr(self.context, SHARING_ATTR, sharing)

    def get_sharing(self):

        return getattr(self.context, SHARING_ATTR, {})

    def edit_list(self):

        editors = [(Allow, 'group:admin', ('view', 'edit')),
                   (Allow, 'group:editors', ('view', 'edit')),
                   ]

        for user_id in self._sharing.get('admin', []):
            editors.append((Allow, user_id, ('view', 'edit')))

        for user_id in self._sharing.get('editors', []):
            editors.append((Allow, user_id, ('view', 'edit')))

        return editors

    def view_list(self):

        viewers = [(Allow, 'group:viewers', 'view')]

        for user_id in self._sharing.get('viewers', []):
            viewers.append((Allow, user_id, 'view'))

        return viewers
