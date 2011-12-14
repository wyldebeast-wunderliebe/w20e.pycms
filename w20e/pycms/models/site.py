from page import Page
from w20e.pycms.interfaces import ISite
from zope.interface import implements


class Site(Page):

    """ Site object """

    implements(ISite)

    def __init__(self, content_id):

        Page.__init__(self, content_id)

