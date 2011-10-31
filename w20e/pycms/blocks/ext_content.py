from base import Block, BlockView
import urllib
from lxml.html import fromstring, tostring


FORM = """
<form>
  <input type="hidden" name="type" value="ext_content"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  URL: <input type="text" name="url" value="${data.get('url', '')}"/><br/>
  Target: <input type="text" name="target" value="${data.get('target', '')}"/><br/>
  Width: <input type="text" name="width" value="${data.get('width', '')}"/><br/>
  Heigth: <input type="text" name="height" value="${data.get('height', '')}"/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class ExternalContentBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "ext_content"


class ExternalContentBlockView(BlockView):

    @property
    def fragment(self):

        handle = urllib.urlopen(self.context['url'])
        content = handle.readlines()
        handle.close()

        elt = fromstring("".join(content))

        return tostring(elt.xpath("//*[@id='%s']" % self.context['target'])[0])
