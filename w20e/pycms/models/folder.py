from .base import BaseFolder


class Folder(BaseFolder):

    """ simple folder """

    @property
    def base_id(self):

        return self._data_['name']

    @property
    def title(self):

        return self._data_['name']
