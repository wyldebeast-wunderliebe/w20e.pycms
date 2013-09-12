from zope.interface import Interface, Attribute


class IBlock(Interface):

    """ Block definition for use in page layout slots """

    id = Attribute("""Unique id""")

    def render(request):
        
        """ Render the HTML for this block """

