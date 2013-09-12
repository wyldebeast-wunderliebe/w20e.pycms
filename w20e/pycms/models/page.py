from zope.interface import implements
from folder import Folder
from interfaces import IPage
from w20e.pycms.layout.base import LayoutMixin


class Page(Folder, LayoutMixin):

    """ Basic Page """

    implements(IPage)

    def __init__(self, content_id, data=None):

        Folder.__init__(self, content_id, data)
        LayoutMixin.__init__(self)

    @property
    def title(self):

        return self.__data__['name']

    @property
    def full_text(self):

        "TODO"
