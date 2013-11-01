from fanstatic import Group, Library, Resource
from fanstatic import get_library_registry
from logging import getLogger

LOGGER = getLogger('w20e.pycms')

class CSSRegistry(object):
    def __init__(self):

        self._registry = {}

    def add(self, name, rootpath, relpath, minifier, target, media):

        # fanstatic library registry
        libreg = get_library_registry()

        for tgt in target.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = Group([])

            library = Library(name, rootpath)
            libreg.add(library)

            css_resource = Resource(library, relpath, minifier=minifier)

            self._registry[tgt].resources.add(css_resource)

    def get(self, target):

        return self._registry.get(target, None)


class JSRegistry(object):
    def __init__(self):

        self._registry = {}

    def add(self, name, rootpath, relpath, minifier, target):

        # fanstatic library registry
        libreg = get_library_registry()

        for tgt in target.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = Group([])

            library = Library(name, rootpath)
            libreg.add(library)

            js_resource = Resource(library, relpath, minifier=minifier)

            self._registry[tgt].resources.add(js_resource)

    def get(self, target):

        return self._registry.get(target, None)


class Admin(object):
    """ Admin utility class """

    def title(self):
        """ title to be used in admin views """

        return "w20e.pycms"

    def brand_title(self):
        """ title of the CMS brand to be used in admin views """

        return "w20e.pycms"
