from folder import Folder
from ..blocks.base import BlockContainer

class Page(Folder, BlockContainer):

    """ Basic Page """

    def __init__(self, content_id):

        Folder.__init__(self, content_id)
        BlockContainer.__init__(self, refs=True)

        self._content = ""

    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self.__data__['text'] or "")

    @property
    def title(self):

        return self.__data__['name']
