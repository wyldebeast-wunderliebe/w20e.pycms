from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import Tokens, PythonIdentifier
from interfaces import ILayouts


class ILayoutDirective(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Unique layout name",
        required=True)

    #title = TextLine(
    #    title=u"Title",        
    #    description=u"Layout title for action",
    #    required=True)

    template = TextLine(
        title=u"Template",
        description=u"path to template, so that Pyramid can find it",
        required=True)

    interface = TextLine(
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


    #title = TextLine(
    #    title=u"Title",
    #    description=u"Slot title",
    #    required=True)


class layout(object):

    """ The layout handler takes care of assigning slots to pages. """

    def __init__(self, context, name, template, **kwargs):

        """ Add a layout to the registry"""

        self.context = context
        self.name = name
        self.template = template
        self.slots = []

        clazz = kwargs['interface']
        path, clazz = ".".join(clazz.split(".")[:-1]), clazz.split(".")[-1]

        exec("from %s import %s" % (path, clazz))

        self.interface = eval(clazz)

        registry = context.context.registry.getUtility(ILayouts)
        registry.register_layout(name, self)

    def slot(self, context, name, blocks):
        self.slots.append(Slot(name, blocks))


class Slot(object):
    
    def __init__(self, name, blocks):

        self.name = name
        self.blocks = blocks


class IBlockDirective(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Unique block name",
        required=True)

    add_form = TextLine(
        title=u"Add form",
        description=u"Add form",
        required=True)

    edit_form = TextLine(
        title=u"Edit form",
        description=u"Edit form",
        required=True)


class Block(object):

    def __init__(self, name, add_form, edit_form):

        self.name = name
        self.add_form = add_form
        self.edit_form = edit_form


def block(_context, name, **kwargs):

    registry = _context.context.registry.getUtility(ILayouts)
    registry.register_block(name, Block(name, kwargs['add_form'], 
                                        kwargs['edit_form']))
