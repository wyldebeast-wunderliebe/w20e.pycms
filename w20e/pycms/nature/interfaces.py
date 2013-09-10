from zope.interface import Interface


class INatures(Interface):

    """ Marker class """

class INature(Interface):

    """ Any content may have a 'nature', like 'news' or 'event'."""
