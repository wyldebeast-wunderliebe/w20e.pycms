from persistent.mapping import PersistentMapping
from zope.interface import implements
from interfaces import IBlock


class Block(PersistentMapping):

    implements(IBlock)

    def __init__(self, block_id, **props):

        super(Block, self).__init__()
        self.id = block_id
        self.update(props)

    def __repr__(self):

        return "%s; %s" % (self.type, self.items())

    @property
    def type(self):

        return self.__class__.__name__.lower()
