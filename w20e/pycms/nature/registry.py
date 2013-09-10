from zope.interface import Interface, providedBy
from interfaces import INatures


def add_natures(event):

    if event['renderer_name'].endswith("nature/templates/action.pt"):

        natures = event['request'].registry.getUtility(INatures)

        valid_natures = []

        for nature in natures.list_natures():

            if nature.get("for_", None):

                if nature['for_'] in providedBy(event['context']):
                    valid_natures.append(nature)
            else:
                valid_natures.append(nature)

        event['natures'] = valid_natures


class Natures(object):

    """ Natures utility tool """

    def __init__(self):

        self.registry = {}

    def register_nature(self, name, nature):

        self.registry[name] = nature

    def get_nature(self, nature_name):

        return self.registry.get(nature_name, None)

    def list_natures(self):

        return self.registry.values()
