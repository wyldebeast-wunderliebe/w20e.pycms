from __future__ import absolute_import
from .base import BaseContent


class File(BaseContent):

    """ File model """

    @property
    def base_id(self):

        return self._data_['data']['name']

    @property
    def title(self):

        return self._data_['name']
