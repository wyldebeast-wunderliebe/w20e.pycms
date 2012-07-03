import os
from w20e.hitman.models.base import BaseContent
from ..utils import resize_image
from ZODB.blob import Blob
from ..utils import package_home


current_folder = package_home(globals())


class Image(BaseContent):

    """ Image model """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'image.xml')

    def _store_resized_image(self, key, data):
        """ store a blob image as attribute """
        blob = Blob()
        f = blob.open('w')
        f.write(data['data'])
        f.close()
        setattr(self, key, blob)
        self._p_changed = 1

    def _get_resized_image(self, key):
        """ retrieve a blob image """
        blob = getattr(self, key)
        return {'name': self.__data__['data']['name'],
                'data': blob}

    @property
    def thumbnail(self):

        """ return the thumbnail, or lazy create it when not present
        yet """
        key = '__cached_blob_thumbnail'
        if not hasattr(self, key):
            self._store_resized_image(key, resize_image(self.__data__['data']))
        return self._get_resized_image(key)

    def get_size(self, size=(800, 600)):

        """ return the resized image, or lazy create it when not present
        yet """

        key = '_cached_blob_%s_%s' % size
        if not hasattr(self, key):
            self._store_resized_image(key, resize_image(
                self.__data__['data'], size))
        return self._get_resized_image(key)

    @property
    def base_id(self):

        return self.__data__['data']['name']

    @property
    def title(self):
        return self.__data__['name']
