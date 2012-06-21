from ..interfaces import IJSRegistry
from ..thirdparty.jsmin import jsmin


class JSView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        jstarget = self.request.path.split("/")[-1].split(".")[0]

        all_js = []

        jsregistry = self.request.registry.getUtility(IJSRegistry)

        for filename in jsregistry.get(jstarget):

            #all_js.append("/* %s */" % filename)
            all_js.append(open(filename).read())
            all_js.append("\n")

        val = self.request.registry.settings.get('pycms.minify_js', False)
        if isinstance(val, str):
            val = val.lower() == 'true'
        if val:
            return jsmin("".join(all_js))

        return "".join(all_js)
