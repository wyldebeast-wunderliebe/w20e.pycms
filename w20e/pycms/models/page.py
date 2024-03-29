from zope.interface import implementer
from .folder import Folder
from ..blocks.base import BlockContainer
from .interfaces import IPage


@implementer(IPage)
class Page(Folder, BlockContainer):

    """ Basic Page """

    def __init__(self, content_id, data=None, **kwargs):

        Folder.__init__(self, content_id, data, **kwargs)
        BlockContainer.__init__(self, refs=True)

        self._content = ""

    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self._data_['text'] or "")

    @property
    def title(self):

        return self._data_['name']
