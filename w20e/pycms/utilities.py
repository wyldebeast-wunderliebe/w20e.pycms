class CSSRegistry(object):

    def __init__(self):

        self._registry = {}


    def add(self, cssfile, csstarget, media):

        for tgt in csstarget.split(","):
            tgt = tgt.strip()

            if not self._registry.has_key(tgt):
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

            if not self._registry.has_key(tgt):
                self._registry[tgt] = []

            self._registry[tgt].append(jsfile)


    def get(self, target):

        return self._registry.get(target, [])
