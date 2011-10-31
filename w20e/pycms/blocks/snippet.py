from base import Block, BlockView


FORM = """
<form>
  <input type="hidden" name="type" value="snippet"/>
  <input type="hidden" name="mode" value="${data.get('mode', 'add')}"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  <textarea name="snippet" rows="10" cols="80">${data.get('snippet', '')}</textarea><br/>
  Width: <input type="text" name="width" value="${data.get('width', '')}"/><br/>
  Heigth: <input type="text" name="height" value="${data.get('height', '')}"/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class SnippetBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "snippet"


class SnippetBlockView(BlockView):

    @property
    def snippet(self):

        return self.context.get('snippet', '')
