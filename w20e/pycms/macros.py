from zope.interface import Interface


class IMacros(Interface):

    """ Marker class """


class Macros(object):

    """ Object actions tool """

    def __init__(self):

        self.registry = {}

    def register_macro(self, name, **kwargs):

        self.registry[name] = kwargs

    def list_macros(self):

        return self.registry.keys()

    def get_macro(self, name):

        return self.registry[name]['ptfile']
