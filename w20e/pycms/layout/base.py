from zope.interface import implements
from interfaces import IBaseLayout


class BaseLayout(object):

    implements(IBaseLayout)

    def __init__(self, page):

        """ Adapt page """
        
        self.context = page

    @property
    def slots(self):

        return [{"name": "text"}]
