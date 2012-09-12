from zope.interface import Interface, Attribute
from w20e.pycms.models.interfaces import ISite


class ICSSRegistry(Interface):

    """ Marker for CSSRegistry """


class IJSRegistry(Interface):

    """ Marker for JSRegistry """


class IACL(Interface):

    """ marker for security """


class IBlobFile(Interface):
    """ Marker for blob file """


class ICatalog(Interface):

    """ Marker for using catalog """


class IMailer(Interface):

    """ Marker class """

class INature(Interface):

    """ Any content may have a 'nature', like 'news' or 'event'."""

class IAdmin(Interface):

    """ provide helper methods for admin interface """

class ITemporaryObject(Interface):

    """ marker interface for temporary objects """
