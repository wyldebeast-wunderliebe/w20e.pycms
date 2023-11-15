
from w20e.pycms.nature import INatures
from w20e.hitman.events import ContentChanged


class NatureView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def add_nature(self):

        nature_id = self.request.params['nature_id']

        natures = self.request.registry.getUtility(INatures)

        nature = natures.get_nature(nature_id)

        if nature:
            self.context.add_nature(nature['interface'])
            self.request.registry.notify(
                ContentChanged(self.context))

        return True

    def remove_nature(self):

        nature_id = self.request.params['nature_id']

        natures = self.request.registry.getUtility(INatures)

        nature = natures.get_nature(nature_id)

        if nature:
            self.context.remove_nature(nature['interface'])
            self.request.registry.notify(
                ContentChanged(self.context))

        return True
