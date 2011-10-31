from zope.interface import Interface
from w20e.hitman.models import Registry


class ICTypes(Interface):

    """ Marker class """


class CTypes(object):

    """ Object actions tool """

    def __init__(self):

        self.registry = {}


    def register_ctype(self, name, **kwargs):

        self.registry[name] = kwargs

        if kwargs.get('factory', None):
            clazz = kwargs['factory']
            path, clazz = ".".join(clazz.split(".")[:-1]), clazz.split(".")[-1]
            
            exec("from %s import %s" % (path, clazz))

            Registry.register(name, eval(clazz))


    def get_ctype_info(self, name):

        return self.registry.get(name, {})
