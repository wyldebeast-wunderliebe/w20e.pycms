from base import Block, BlockView

FORM = """
<form>
  <input type="hidden" name="type" value="feed"/>
  <input type="hidden" name="mode" value="${data.get('mode', 'add')}"/>
  ID: <input type="text" name="id" value="${data.get('id', '')}"/><br/>
  Feed URL: <input type="text" name="feedurl" value="${data.get('feedurl', '')}"/><br/>
  Width: <input type="text" name="width" size="4" value="${data.get('width', '')}"/><br/>
  Heigth: <input type="text" name="height" size="4" value="${data.get('height', '')}"/><br/>
  Items: <input type="text" name="items" size="4" value="${data.get('items', '')}"/>
  <input type="submit" value="Save"/>
  <input type="button" name="cancel" value="Cancel"/>
</form>
"""


class FeedBlock(Block):

    add_form = edit_form = FORM

    def __init__(self, block_id, **props):

        Block.__init__(self, block_id, **props)

        self.type = "rssfeed"


class FeedBlockView(BlockView):

    @property
    def feedurl(self):

        return self.context.get('feedurl', '')


    def __call__(self):

        return {'tgt': '%s_content' % self.id, 
                'feedurl': self.feedurl, 
                'items': self.context.get('items', 10)}
