from zope.interface import implements
from page import Page
from interfaces import ISite


class Site(Page):

    """ Site object """

    implements(ISite)

    def __init__(self, content_id, data=None):

        Page.__init__(self, content_id, data)

    @property
    def cms_version(self):
        return 'PyCMS version: %s' % getattr(self, 'pycms_version', 'unknown')
