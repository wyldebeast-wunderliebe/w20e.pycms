from .page import Page
from zope.interface import implementer_only, implementer
from w20e.hitman.models.base import IFolder
from .interfaces import ISite


# @implementer_only(ISite, IFolder)
@implementer(ISite, IFolder)
class Site(Page):

    """ Site object """

    @property
    def cms_version(self):
        return 'PyCMS version: %s' % getattr(self, 'pycms_version', 'unknown')
