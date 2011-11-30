from blocks.base import *
from blocks.text import TextBlock
from blocks.snippet import SnippetBlock
from blocks.image import ImageBlock
from blocks.feed import FeedBlock
from blocks.ext_content import ExternalContentBlock
from lxml.html import fromstring, tostring
from blocks.registry import Registry


class Parser(object):

    def __init__(self, page):

        self._page = page

    def parse(self, frag):

        # wrap frag with container...
        elt = fromstring('<div id="content">' + frag + '</div>')

        for child in elt.iterchildren(tag="div"):

            cfg = self._get_config(child)
            clazz = Registry.get_type(cfg.get('type', None))

            if not clazz:
                continue

            block = clazz(child.get("id"), **cfg)
            self._page.add_block(block)

    def _get_config(self, elt):

        cfg = {}

        if not len(elt.find("dl")):

            return cfg

        for key in elt.find("dl").iterchildren("dt"):

            cfg[key.text] = tostring(key.getnext())[4:-5]

        return cfg
