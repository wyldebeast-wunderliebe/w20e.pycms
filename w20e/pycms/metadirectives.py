from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalObject
from w20e.pycms.interfaces import ICSSRegistry, IJSRegistry
from actions import IActions
from ctypes import ICTypes
from macros import IMacros
from index import IIndexes


class ICSSDirective(Interface):
    """ Collect css files into one """

    name = TextLine(
        title=u"Library name",
        description=u"Unique name of library",
        required=True)

    rootpath = TextLine(
        title=u"Library Path",
        description=u"Relative path to CSS files",
        required=True)

    relpath = TextLine(
        title=u"CSS File",
        description=u"Relative path to CSS file",
        required=True)

    minifier = TextLine(
        title=u"CSS Minifier",
        description=u"Type of CSS minifier used",
        required=False)

    target = TextLine(
        title=u"CSS target(s)",
        description=u"Target css name as called from client.",
        required=True)

    media = TextLine(
        title=u"Media",
        description=u"For media (screen, print, ...)",
        required=False)

    depends = TextLine(
        title=u"List of dependencies",
        description=u"Dependencies (comma separated) this CSS file depends on.",
        required=False)


def css(_context, name, rootpath, relpath, target, depends=None, minifier='cssmin', media="screen"):
    reg = _context.context.registry
    cssregistry = reg.getUtility(ICSSRegistry)

    cssregistry.add(name, rootpath, relpath, minifier, target, depends, media)


class IJSDirective(Interface):
    """ Collect js files into one """

    name = TextLine(
        title=u"Library name",
        description=u"Unique name of library",
        required=True)

    rootpath = TextLine(
        title=u"JS File",
        description=u"Relative path to JS file.",
        required=True)

    relpath = TextLine(
        title=u"JS target",
        description=u"Target js name as called from client.",
        required=True)

    minifier = TextLine(
        title=u"JS Minifier",
        description=u"Type of JS minifier used",
        required=False)

    target = TextLine(
        title=u"JS target(s)",
        description=u"Target js name as called from client.",
        required=True)

    depends = TextLine(
        title=u"List of dependencies",
        description=u"Dependencies (comma separated) this JS file depends on.",
        required=False)


def js(_context, name, rootpath, relpath, target, depends=None, minifier='jsmin'):
    reg = _context.context.registry
    jsregistry = reg.getUtility(IJSRegistry)

    jsregistry.add(name, rootpath, relpath, minifier, target, depends)


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

    factory = GlobalObject(
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
