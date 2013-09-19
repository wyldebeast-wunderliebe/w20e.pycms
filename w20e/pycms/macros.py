from zope.interface import Interface
from pyramid.renderers import get_renderer


def add_macros(event):

    macros = event['request'].registry.getUtility(IMacros)

    for macro in macros.list_macros():
        
        event[macro] = get_renderer(
            macros.get_macro(macro)).implementation()


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
