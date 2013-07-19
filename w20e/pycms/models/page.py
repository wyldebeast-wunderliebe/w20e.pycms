from zope.interface import implements, providedBy, alsoProvides, \
    noLongerProvides
from folder import Folder
from interfaces import IPage


class Page(Folder):

    """ Basic Page """

    implements(IPage)

    def __init__(self, content_id, data=None):

        Folder.__init__(self, content_id, data)

    @property
    def full_text(self):

        # TODO: handle page complex layout!

        return "%s %s" % (self.title, self.__data__['text'] or "")

    @property
    def title(self):

        return self.__data__['name']

    def has_layout(self, layout):
        
        return layout.interface in providedBy(self)

    def set_layout(self, layout):

        """ Remove existing layout interfaces, and set to current. """

        for i in [i for i in providedBy(self) if i.extends(ILayout)]:

            noLongerProvides(self, i)

        alsoProvides(self, layout)
