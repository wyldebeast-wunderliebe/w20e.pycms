from .base import BaseContent


class Form(BaseContent):

    """ Generic Form """

    def __init__(self, content_id, data=None):

        BaseContent.__init__(self, content_id, data)

    @property
    def base_id(self):

        return self._data_['name']

    @property
    def title(self):

        return self._data_['name']
