from zope.interface import implements, Attribute, Interface


class IAppRootReady(Interface):

    """ Application is initialized and (almost) ready to serve..."""

    app_root = Attribute("The application root object")
    settings = Attribute("The application settings")


class ITemporaryObjectCreated(Interface):

    """ Temporary Object has been created..."""

    object = Attribute("The temporary object")


class ITemporaryObjectFinalized(Interface):

    """ Temporary Object has been finalized..."""

    object = Attribute("The temporary object")


class AppRootReady(object):

    implements(IAppRootReady)

    def __init__(self, app_root, registry):

        self.app_root = app_root
        self.registry = registry


class TemporaryObjectCreated(object):

    implements(ITemporaryObjectCreated)

    def __init__(self, object):

        self.object = object


class TemporaryObjectFinalized(object):

    implements(ITemporaryObjectFinalized)

    def __init__(self, object):

        self.object = object
