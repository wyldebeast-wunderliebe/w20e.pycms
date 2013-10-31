from w20e.pycms.interfaces import ICSSRegistry

def pycms_fanstatic_factory(handler, registry):

    def pycms_fanstatic_injector(request):

        response = handler(request)

        # this needs to be defined in the template, e.g. ${request.environ.update({'pycms_fanstatic_target':'public'})}
        # optional targets are 'public' and 'manage'

        target = request.environ.get('pycms_fanstatic_target')

        if target:
            cssregistry = request.registry.getUtility(ICSSRegistry)
            resource = cssregistry.get(target)
            if resource:
                resource.need()

        return response

    return pycms_fanstatic_injector
