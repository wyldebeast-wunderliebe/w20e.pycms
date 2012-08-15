from page import Page
from zope.interface import implementsOnly
from w20e.hitman.models.base import IFolder
from interfaces import ISite



class Site(Page):

    """ Site object """

    implementsOnly(ISite, IFolder)

    def __init__(self, content_id):

        Page.__init__(self, content_id)

    @property
    def cms_version(self):
        return 'PyCMS version: %s' % getattr(self, 'pycms_version', 'unknown')
