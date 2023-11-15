
from zope.interface import Attribute, Interface, implementer


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


@implementer(IAppRootReady)
class AppRootReady(object):

    def __init__(self, app_root, registry):

        self.app_root = app_root
        self.registry = registry


@implementer(ITemporaryObjectCreated)
class TemporaryObjectCreated(object):

    def __init__(self, object, request=None):

        self.object = object
        self.request = request


@implementer(ITemporaryObjectFinalized)
class TemporaryObjectFinalized(object):

    def __init__(self, object, request=None):

        self.object = object
        self.request = request
