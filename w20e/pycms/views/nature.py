from w20e.pycms.nature import INatures


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

        return True

    def remove_nature(self):

        nature_id = self.request.params['nature_id']

        natures = self.request.registry.getUtility(INatures)

        nature = natures.get_nature(nature_id)

        if nature:
            self.context.remove_nature(nature['interface'])

        return True
