from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import Tokens, PythonIdentifier, GlobalObject
from interfaces import ILayouts


class ILayoutDirective(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Unique layout name",
        required=True)

    template = TextLine(
        title=u"Template",
        description=u"path to template, so that Pyramid can find it",
        required=True)

    interface = GlobalObject(
        title=u"Interface",
        description=u"Marker interface for this layout. FULL path required",
        required=True)


class ILayoutSlotDirective(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Slot name",
        required=True)

    blocks = Tokens(
        title=u"Blocks",
        description=u"Allowed blocks",
        required=False,
        value_type=PythonIdentifier()
        )


class layout(object):

    """ The layout handler takes care of assigning slots to pages. """

    def __init__(self, context, name, template, interface):

        """ Add a layout to the registry"""

        self.name = name
        self.template = template
        self.slots = []
        self.interface = interface

        registry = context.context.registry.getUtility(ILayouts)
        registry.register_layout(name, self)

    def slot(self, context, name, blocks):
        self.slots.append(Slot(name, blocks))


class Slot(object):
    
    def __init__(self, name, blocks):

        self.name = name
        self.blocks = blocks
