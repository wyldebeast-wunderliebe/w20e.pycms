from zope.interface import implements, providedBy, alsoProvides, \
    noLongerProvides
from collections import OrderedDict
from persistent.mapping import PersistentMapping
from interfaces import IBaseLayout, ILayoutMixin, ILayout


class BaseLayout(object):

    implements(IBaseLayout)

    def __init__(self, page):

        """ Adapt page """

        self.context = page

    @property
    def slots(self):

        return [{"name": "text"}]


class LayoutMixin(object):

    implements(ILayoutMixin)

    def __init__(self):

        self._blocks = PersistentMapping()

    def has_layout(self, layout):

        return layout.interface in providedBy(self)

    def set_layout(self, layout):

        """ Remove existing layout interfaces, and set to current. """

        for i in [i for i in providedBy(self) if i.extends(ILayout)]:

            noLongerProvides(self, i)

        alsoProvides(self, layout.interface)

    def save_block(self, slot, block_id, block):

        if slot not in self._blocks.keys():
            self._blocks[slot] = OrderedDict()
        self._blocks[slot][block_id] = block

    def get_block(self, slot_id, block_id):

        return self._blocks[slot_id][block_id]

    def rm_block(self, slot_id, block_id):

        del self._blocks[slot_id][block_id]

    def get_blocks(self, slot_id):

        try:
            return self._blocks[slot_id].values()
        except:
            return []
