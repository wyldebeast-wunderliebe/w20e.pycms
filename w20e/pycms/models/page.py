from persistent.mapping import PersistentMapping
from collections import OrderedDict
from zope.interface import implements, providedBy, alsoProvides, \
    noLongerProvides
from folder import Folder
from interfaces import IPage
from w20e.pycms.layout.interfaces import ILayout


class Page(Folder):

    """ Basic Page """

    implements(IPage)

    def __init__(self, content_id, data=None):

        Folder.__init__(self, content_id, data)
        self._blocks = PersistentMapping()

    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self.__data__['text'] or "")

    @property
    def title(self):

        return self.__data__['name']

    def has_layout(self, layout):

        return layout.interface in providedBy(self)

    def set_layout(self, layout):

        """ Remove existing layout interfaces, and set to current. """

        for i in [i for i in providedBy(self) if i.extends(ILayout)]:

            noLongerProvides(self, i)

        alsoProvides(self, layout.interface)

    def save_block(self, slot, block_id, block):

        if not slot in self._blocks.keys():
            self._blocks[slot] = OrderedDict()
        self._blocks[slot][block_id] = block
        self._blocks._p_changed
        self._p_changed

    def get_block(self, slot_id, block_id):

        return self._blocks[slot_id][block_id]

    def rm_block(self, slot_id, block_id):
        
        del self._blocks[slot_id][block_id]

    def get_blocks(self, slot_id):

        return self._blocks[slot_id].values()
