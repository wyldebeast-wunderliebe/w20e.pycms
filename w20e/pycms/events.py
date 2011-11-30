from zope.interface import implements, Attribute, Interface


class IAppRootReady(Interface):

    """ Application is initialized and (almost) ready to serve..."""

    app_root = Attribute("The application root object")


class AppRootReady(object):

    implements(IAppRootReady)

    def __init__(self, app_root):

        self.app_root = app_root
