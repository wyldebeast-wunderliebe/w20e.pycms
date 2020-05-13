from builtins import object
from zope.interface import Interface
from w20e.hitman.models import Registry
from pyramid.path import DottedNameResolver


class ICTypes(Interface):

    """ Marker class """


class CTypes(object):

    """ Object actions tool """

    def __init__(self):

        self.registry = {}

    def register_ctype(self, name, **kwargs):

        if name in self.registry:
            self.registry[name].update(kwargs)
        else:
            self.registry[name] = kwargs

        if kwargs.get('factory', None):
            clazz = kwargs['factory']
            klass = DottedNameResolver().resolve(clazz)
            Registry.register(name, klass)

    def get_ctype_info(self, name):

        return self.registry.get(name, {})

