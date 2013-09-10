from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalObject
from interfaces import INatures


class INatureDirective(Interface):

    """ Register Content type info """

    name = TextLine(
        title=u"Type",
        description=u"Unique name",
        required=True)

    i18n_msgid = TextLine(
        title=u"i18n_msgid",
        description=u"i18n translation id",
        required=False)

    interface = TextLine(
        title=u"Interface",
        description=u"Marker interface for this nature. FULL path required",
        required=True)

    for_ = GlobalObject(
        title=(u"The interface or class this nature is for. Specify FULL path"),
        required=False
        )

def nature(_context, name, **kwargs):

    reg = _context.context.registry
    nature_registry = reg.getUtility(INatures)

    nature_registry.register_nature(name, **kwargs)

