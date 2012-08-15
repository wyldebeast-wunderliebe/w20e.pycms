from zope.interface import Interface, providedBy


def add_natures(event):

    if event['renderer_name'].endswith("action_nature.pt"):

        natures = event['request'].registry.getUtility(INatures)

        valid_natures = []

        for nature in natures.list_natures():

            if nature.get("for_", None):

                if nature['for_'] in providedBy(event['context']):
                    valid_natures.append(nature)
            else:
                valid_natures.append(nature)

        event['natures'] = valid_natures


class INatures(Interface):

    """ Marker class """


class Natures(object):

    """ Natures utility tool """

    def __init__(self):

        self.registry = {}

    def register_nature(self, name, **kwargs):

        """ TODO: add i18n_msgid """

        clazz = kwargs['interface']
        path, clazz = ".".join(clazz.split(".")[:-1]), clazz.split(".")[-1]

        exec("from %s import %s" % (path, clazz))

        kwargs['interface'] = eval(clazz)
        kwargs['name'] = name

        if kwargs.get("_for", None):

            clazz = kwargs['_for']
            
            path, clazz = ".".join(clazz.split(".")[:-1]), clazz.split(".")[-1]

            exec("from %s import %s" % (path, clazz))
            
            kwargs['_for'] = eval(clazz)

        self.registry[name] = kwargs

    def get_nature(self, nature_name):

        return self.registry.get(nature_name, None)

    def list_natures(self):

        return self.registry.values()
