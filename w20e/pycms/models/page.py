import os
from folder import Folder
from ..blocks.base import BlockContainer
from ..utils import package_home


current_folder = package_home(globals())


class Page(Folder, BlockContainer):

    """ Basic Page """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'page.xml')

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
