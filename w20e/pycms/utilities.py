class CSSRegistry(object):

    def __init__(self):

        self._registry = {}

    def add(self, cssfile, csstarget, media):

        for tgt in csstarget.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = []

            self._registry[tgt].append((cssfile, media))

    def get(self, target):

        return self._registry.get(target, [])


class JSRegistry(object):

    def __init__(self):

        self._registry = {}

    def add(self, jsfile, jstarget):

        for tgt in jstarget.split(","):
            tgt = tgt.strip()

            if not tgt in self._registry:
                self._registry[tgt] = []

            self._registry[tgt].append(jsfile)

    def get(self, target):

        return self._registry.get(target, [])


class Admin(object):
    """ Admin utility class """

    def title(self):
        """ title to be used in admin views """

        return "w20e.pycms"

    def brand_title(self):
        """ title of the CMS brand to be used in admin views """

        return "w20e.pycms"
