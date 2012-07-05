from zope.interface import Interface
from zope.schema import TextLine
from interfaces import ICSSRegistry, IJSRegistry
import os
from actions import IActions
from ctypes import ICTypes
from macros import IMacros
from index import IIndexes


def find_file(filename, context):

    """ If file is relative, unrelate... """

    if filename[0] == "/":

        return filename

    return os.path.join(context.package.__path__[0], filename)


class ICSSDirective(Interface):

    """ Collect css files into one """

    cssfile = TextLine(
        title=u"CSS File",
        description=u"Relative path to CSS file.",
        required=True)

    csstarget = TextLine(
        title=u"CSS target(s)",
        description=u"Target css name as called from client.",
        required=True)

    media = TextLine(
        title=u"Media",
        description=u"For media (screen, print, ...)",
        required=False)


def css(_context, cssfile, csstarget, media="screen"):

    reg = _context.context.registry
    cssregistry = reg.getUtility(ICSSRegistry)

    filename = find_file(cssfile, _context)

    cssregistry.add(filename, csstarget, media)


class IJSDirective(Interface):

    """ Collect js files into one """

    jsfile = TextLine(
        title=u"JS File",
        description=u"Relative path to JS file.",
        required=True)

    jstarget = TextLine(
        title=u"JS target",
        description=u"Target js name as called from client.",
        required=True)


def js(_context, jsfile, jstarget):

    reg = _context.context.registry
    cssregistry = reg.getUtility(IJSRegistry)

    filename = find_file(jsfile, _context)

    cssregistry.add(filename, jstarget)


class IActionDirective(Interface):

    """ Actions """

    name = TextLine(
        title=u"Name",
        description=u"Unique action name",
        required=True)

    label = TextLine(
        title=u"Label",
        description=u"Label to show",
        required=False)

    icon = TextLine(
        title=u"Icon class as used by Awesome Fonts",
        description=u"Icon class",
        required=False)    

    target = TextLine(
        title=u"Target",
        description=u"Usually http href",
        required=True)

    category = TextLine(
        title=u"Category",
        description=u"Action is of this category",
        required=True)

    ctype = TextLine(
        title=u"Content type",
        description=u"Action applies only to this (these) content type(s)",
        required=False)

    permission = TextLine(
        title=u"Permission",
        description=u"Permission",
        required=False)

    condition = TextLine(
        title=u"Condition",
        description=u"Condition",
        required=False)

    template = TextLine(
        title=u"Template",
        description=u"Template to use for rendering",
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
        title=u"Type",
        description=u"Unique type name, lowercase",
        required=True)

    factory = TextLine(
        title=u"Factory",
        description=u"Factory that creates this type",
        required=False)

    icon = TextLine(
        title=u"icon",
        description=u"Path to icon",
        required=False)

    subtypes = TextLine(
        title=u"subtypes",
        description=u"List of subtypes",
        required=False)


def ctype(_context, name, **kwargs):

    reg = _context.context.registry
    ctype_registry = reg.getUtility(ICTypes)

    ctype_registry.register_ctype(name, **kwargs)


class IMacroDirective(Interface):

    """ Register Content type info """

    name = TextLine(
        title=u"name",
        description=u"Register as...",
        required=True)

    ptfile = TextLine(
        title=u"Template",
        description=u"PT file",
        required=True)


def macro(_context, name, **kwargs):

    reg = _context.context.registry
    macro_registry = reg.getUtility(IMacros)

    macro_registry.register_macro(name, **kwargs)


class IIndexDirective(Interface):

    """ Register index """

    name = TextLine(
        title=u"Index name",
        description=u"Index id",
        required=True)

    field = TextLine(
        title=u"Field name",
        description=u"Index field",
        required=True)

    idxtype = TextLine(
        title=u"Type",
        description=u"Index type",
        required=True)


def index(_context, name, field, idxtype, **kwargs):

    reg = _context.context.registry
    indexes = reg.getUtility(IIndexes)

    indexes.register_index(name, field, idxtype, **kwargs)
