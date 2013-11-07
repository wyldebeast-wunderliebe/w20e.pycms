import fanstatic
from fanstatic.inclusion import Inclusion
from w20e.pycms.interfaces import ICSSRegistry, IJSRegistry
from logging import getLogger
from js.jquery import jquery

LOGGER = getLogger('w20e.pycms')

def pycms_fanstatic_factory(handler, registry):
    def pycms_fanstatic_injector(request):

        response = handler(request)

        # fetch jquery through fanstatic
        jquery.need()

        # this needs to be defined in the template, e.g.
        #     ${request.environ.update({'pycms_fanstatic_target':'public'})}
        # optional targets are 'public' and 'manage'
        target = request.environ.get('pycms_fanstatic_target')

        if target:
            cssregistry = request.registry.getUtility(ICSSRegistry)
            jsregistry = request.registry.getUtility(IJSRegistry)

            cssresource = cssregistry.get(target)
            if cssresource:
                cssresource.need()

            jsresource = jsregistry.get(target)
            if jsresource:
                jsresource.need()

        return response

    return pycms_fanstatic_injector
