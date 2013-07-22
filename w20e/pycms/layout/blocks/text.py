from base import Block, BlockView, BlockEdit


class Text(Block):

    """ Text block """

    def render(self):

        return self['text']
