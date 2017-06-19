import pkg_resources
from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalObject
from .interfaces import ICSSRegistry, IJSRegistry
import os
from .actions import IActions
from .ctypes import ICTypes
from .macros import IMacros
from .index import IIndexes
from .nature import INatures


def find_file(filename, context):

    """ If file is relative, unrelate... """

    if filename[0] != "/":

        if ":" in filename:
            module, resource = filename.split(":")
        
            provider = pkg_resources.get_provider(module)
        
            filename = provider.get_resource_filename(module, resource)
        else:
            filename = os.path.join(context.package.__path__[0], filename)
                    
    return filename


class ICSSDirective(Interface):

    """ Collect css files into one """

    cssfile = TextLine(
        title="CSS File",
        description="Relative path to CSS file.",
        required=True)

    csstarget = TextLine(
        title="CSS target(s)",
        description="Target css name as called from client.",
        required=True)

    media = TextLine(
        title="Media",
        description="For media (screen, print, ...)",
        required=False)


def css(_context, cssfile, csstarget, media="screen"):

    reg = _context.context.registry
    cssregistry = reg.getUtility(ICSSRegistry)

    filename = find_file(cssfile, _context)

    cssregistry.add(filename, csstarget, media)


class IJSDirective(Interface):

    """ Collect js files into one """

    jsfile = TextLine(
        title="JS File",
        description="Relative path to JS file.",
        required=True)

    jstarget = TextLine(
        title="JS target",
        description="Target js name as called from client.",
        required=True)


def js(_context, jsfile, jstarget):

    reg = _context.context.registry
    cssregistry = reg.getUtility(IJSRegistry)

    filename = find_file(jsfile, _context)

    cssregistry.add(filename, jstarget)


class IActionDirective(Interface):

    """ Actions """

    name = TextLine(
        title="Name",
        description="Unique action name",
        required=True)

    label = TextLine(
        title="Label",
        description="Label to show",
        required=False)

    icon = TextLine(
        title="Icon class as used by Awesome Fonts",
        description="Icon class",
        required=False)    

    target = TextLine(
        title="Target",
        description="Usually http href",
        required=True)

    category = TextLine(
        title="Category",
        description="Action is of this category",
        required=True)

    ctype = TextLine(
        title="Content type",
        description="Action applies only to this (these) content type(s)",
        required=False)

    permission = TextLine(
        title="Permission",
        description="Permission",
        required=False)

    condition = TextLine(
        title="Condition",
        description="Condition",
        required=False)

    template = TextLine(
        title="Template",
        description="Template to use for rendering",
        required=False)    


def action(_context, name, target, category, label=None, icon=None, ctype=[],
           permission="", condition=None,
           template="w20e.pycms:templates/action.pt"):

    reg = _context.context.registry
    action_registry = reg.getUtility(IActions)

    action_registry.register_action(name, target, category,
                                    label=label,
                                    icon=icon,
                                    ctype=ctype,
                                    permission=permission,
                                    condition=condition,
                                    template=template)


class ICTypeDirective(Interface):

    """ Register Content type info """

    name = TextLine(
        title="Type",
        description="Unique type name, lowercase",
        required=True)

    factory = TextLine(
        title="Factory",
        description="Factory that creates this type",
        required=False)

    icon = TextLine(
        title="icon",
        description="Path to icon",
        required=False)

    subtypes = TextLine(
        title="subtypes",
        description="List of subtypes",
        required=False)


def ctype(_context, name, **kwargs):

    reg = _context.context.registry
    ctype_registry = reg.getUtility(ICTypes)

    ctype_registry.register_ctype(name, **kwargs)


class INatureDirective(Interface):

    """ Register Content type info """

    name = TextLine(
        title="Type",
        description="Unique name",
        required=True)

    i18n_msgid = TextLine(
        title="i18n_msgid",
        description="i18n translation id",
        required=False)

    interface = TextLine(
        title="Interface",
        description="Marker interface for this nature. FULL path required",
        required=True)

    for_ = GlobalObject(
        title=("The interface or class this nature is for. Specify FULL path"),
        required=False
        )

def nature(_context, name, **kwargs):

    reg = _context.context.registry
    nature_registry = reg.getUtility(INatures)

    nature_registry.register_nature(name, **kwargs)


class IMacroDirective(Interface):

    """ Register Content type info """

    name = TextLine(
        title="name",
        description="Register as...",
        required=True)

    ptfile = TextLine(
        title="Template",
        description="PT file",
        required=True)


def macro(_context, name, **kwargs):

    reg = _context.context.registry
    macro_registry = reg.getUtility(IMacros)

    macro_registry.register_macro(name, **kwargs)


class IIndexDirective(Interface):

    """ Register index """

    name = TextLine(
        title="Index name",
        description="Index id",
        required=True)

    field = TextLine(
        title="Field name",
        description="Index field",
        required=True)

    idxtype = TextLine(
        title="Type",
        description="Index type",
        required=True)


def index(_context, name, field, idxtype, **kwargs):

    reg = _context.context.registry
    indexes = reg.getUtility(IIndexes)

    indexes.register_index(name, field, idxtype, **kwargs)
