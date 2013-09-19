from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalObject
from w20e.pycms.layout.interfaces import ILayouts


class IBlockDirective(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Unique block name",
        required=True)
    
    factory = GlobalObject(
        title=u"Factory",
        description=u"A factory used to create the block.",
        required=True,
        )


def block(_context, name, factory):

    registry = _context.context.registry.getUtility(ILayouts)
    registry.register_block(name, factory)
