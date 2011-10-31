from base import Block, BlockView
from registry import Registry


FORM = """
<form target="img_save" action="save_block" method="POST" enctype="multipart/form-data">
  <input type="hidden" name="type" value="image"/>
  <input type="hidden" name="img_url" value="${data.get('img_url', '')}"/>
  <input type="hidden" name="mode" value="${data.get('mode', 'add')}"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  Image: <input tal:condition="data.get('mode', '') != 'edit'" type="file" name="img"/><span tal:condition="data.get('mode', '') == 'edit'">${data.get('img_url', '')}</span>
  <br/>
  Width: <input type="text" name="width" value="${data.get('width', '')}"/><br/>
  Heigth: <input type="text" name="height" value="${data.get('height', '')}"/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
<iframe name="img_save" id="img_save" style="display: none"></iframe>
"""


class ImageBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "image"


class ImageBlockView(BlockView):

    @property
    def img_url(self):

        return self.context.get('img_url', '')


Registry.register_type("image", ImageBlock)
