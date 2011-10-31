class Registry:

    """ Global registry for forms """

    types = {}


    @staticmethod
    def register_type(name, factory):

        Registry.types[name] = factory


    @staticmethod
    def get_type(name):

        return Registry.types.get(name, None)


    @staticmethod
    def list_types():

        return Registry.types.keys()
