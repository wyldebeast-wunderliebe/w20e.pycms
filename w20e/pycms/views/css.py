from ..interfaces import ICSSRegistry
import cssmin


class CSSView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def __call__(self):

        csstarget = self.request.path.split("/")[-1].split(".")[0]

        all_css = []

        cssregistry = self.request.registry.getUtility(ICSSRegistry)

        for filename, media in cssregistry.get(csstarget):

            all_css.append(open(filename).read())

        val = self.request.registry.settings.get('pycms.minify_css', False)
        if isinstance(val, str):
            val = val.lower() == 'true'
        if val:
            return cssmin.cssmin("".join(all_css))

        return "".join(all_css)
