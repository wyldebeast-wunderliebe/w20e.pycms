from base import Block, BlockView
from pyramid.view import render_view


FORM = """
<form>
  <input type="hidden" name="type" value="ref"/>
  <input type="hidden" name="mode" value="${data.get('mode', 'add')}"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  <!-- ref finder goes here -->
  <select class="reffinder" name="ref"/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class RefBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "ref"        


class RefBlockView(BlockView):

    def __call__(self):
        
        block = self._find_block()

        if block:
            return {'content': render_view(block, self.request)}
        else:
            return {'content': 'Not found'}


    def _find_block(self):

        return None
