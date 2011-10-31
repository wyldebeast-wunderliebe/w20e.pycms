from folder import BaseFolder
from ..blocks.base import BlockContainer


class Page(BaseFolder, BlockContainer):

    """ Software project representation """

    add_form = edit_form = "../forms/page.xml"

    def __init__(self, content_id):

        BaseFolder.__init__(self, content_id)
        BlockContainer.__init__(self, refs=True)

        self._content = ""


    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self.__data__['text'])
