from zope.interface import implements
from folder import Folder
from ..blocks.base import BlockContainer
from interfaces import IPage


class Page(Folder, BlockContainer):

    """ Basic Page """

    implements(IPage)

    def __init__(self, content_id, data=None):

        Folder.__init__(self, content_id, data)
        BlockContainer.__init__(self, refs=True)

        self._content = ""

    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self.__data__['text'] or "")

    @property
    def title(self):

        return self.__data__['name']
