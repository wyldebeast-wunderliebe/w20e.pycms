from zope.interface import Interface


class IContent(Interface):

    """ Very base content """


class IFolder(IContent):

    """ Folderish """


class IPage(IFolder):

    """ Marker for page """


class ISite(IPage):

    """ Marker for site"""
