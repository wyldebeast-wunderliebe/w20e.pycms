from page import Page
from w20e.pycms.interfaces import ISite
from zope.interface import implements
from ..security import ACL


class Site(Page):

    """ Site object """

    implements(ISite)


    def __init__(self, content_id):

        Page.__init__(self, content_id)
        self.acl = ACL()


    def add_user(self, data):
        
        self.acl.create_user(**data.as_dict())
