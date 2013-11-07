from fanstatic import Group, Library, Resource
from fanstatic import get_library_registry
from logging import getLogger
from js.jquery import jquery

LOGGER = getLogger('w20e.pycms')


class CSSRegistry(object):
    def __init__(self):

        self._registry = {}

    def add(self, name, rootpath, relpath, minifier, target, depends, media):

        # global fanstatic library registry
        libreg = get_library_registry()

        for tgt in target.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = Group([])

            if name not in libreg.keys():
                LOGGER.info("Create CSS library %s located at %s" % (name, rootpath))
                libreg.add(Library(name, rootpath))

            depends_list = []
            if depends:
                for dependency in depends.split(','):
                    depends_list.append(libreg.get(name).known_resources.get(dependency))

            css_resource = Resource(libreg.get(name), relpath, depends=depends_list, minifier=minifier)

            self._registry[tgt].resources.add(css_resource)

    def get(self, target):

        return self._registry.get(target, None)


class JSRegistry(object):
    def __init__(self):

        self._registry = {}

    def add(self, name, rootpath, relpath, minifier, target, depends):

        # fanstatic library registry
        libreg = get_library_registry()

        for tgt in target.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = Group([])

            if name not in libreg.keys():
                LOGGER.info("Create JS library %s located at %s" % (name, rootpath))
                libreg.add(Library(name, rootpath))

            depends_list = [jquery, ]
            if depends:
                for dependency in depends.split(','):
                    depends_list.append(libreg.get(name).known_resources.get(dependency))

            js_resource = Resource(libreg.get(name), relpath, depends=depends_list, minifier=minifier)

            # TODO move (jquery) dependencies to config
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
