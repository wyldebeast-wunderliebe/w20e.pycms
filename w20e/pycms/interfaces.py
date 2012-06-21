from zope.interface import Interface


class ICSSRegistry(Interface):

    """ Marker for CSSRegistry """


class IJSRegistry(Interface):

    """ Marker for JSRegistry """


class IACL(Interface):

    """ marker for security """


class ISite(Interface):
    """ Marker for Site """


class IBlobFile(Interface):
    """ Marker for blob file """


class ICatalog(Interface):

    """ Marker for using catalog """


class IMailer(Interface):

    """ Marker class """

