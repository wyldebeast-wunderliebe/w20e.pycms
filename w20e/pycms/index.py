from zope.interface import Interface


class IIndexes(Interface):

    """ Marker class """


class Indexes(object):

    """ Object actions tool """

    def __init__(self):

        self.registry = {}

    def register_index(self, field, idxtype):

        self.registry[field] = {'type': idxtype}

    def get_indexes(self):

        return self.registry.items()
