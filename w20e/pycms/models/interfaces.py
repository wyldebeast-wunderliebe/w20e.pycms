from zope.interface import Interface


class IPage(Interface):

    """ Marker for page """


class ISite(Interface):

    """ Marker for site"""


class IPyCMSMixin(Interface):

    """ Marker for Pycms Content Type """
