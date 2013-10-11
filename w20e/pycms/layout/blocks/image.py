from base import Block


class Image(Block):

    """ Text block """

    def render(self, request):

        return """<img src=""/>"""

    def add_url(self, slot):

        return "/xplore"
