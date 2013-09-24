from zope.interface import Interface


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

    def get_ctype_info(self, name):

        return self.registry.get(name, {})

    def get_factory(self, name):

        return self.registry[name].get('factory', None)
