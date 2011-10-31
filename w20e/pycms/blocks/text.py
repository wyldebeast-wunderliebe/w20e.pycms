from base import Block, BlockView
from registry import Registry


FORM = """
<form>
  <input type="hidden" name="type" value="text"/>
  <input type="hidden" name="mode" value="${data.get('mode', 'add')}"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  <textarea class="wysiwyg" name="txt">${data.get('txt', '')}</textarea><br/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class TextBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "text"


class TextBlockView(BlockView):

    @property
    def text(self):

        return self.context.get('txt', '')


Registry.register_type("text", TextBlock)
