from base import Block


class Text(Block):

    """ Text block """

    def render(self):

        return self['text']
