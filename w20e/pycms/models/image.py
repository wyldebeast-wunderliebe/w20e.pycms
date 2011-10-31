import mimetypes
#from ..blobfile import File
from w20e.hitman.models.base import BaseContent
from ..utils import resize_image
from ZODB.blob import Blob
from w20e.forms.formdata import FormData
from w20e.forms.data.field import Field


class Image(BaseContent):

    """ Image model """

    add_form = edit_form = "../forms/image.xml"


    def __init__(self, content_id, data=None):

        BaseContent.__init__(self, content_id)
        self.__data__['data'] = Blob()
        if data:
            self.data = data
        self._p_changed = 1

    def store_data(self, form, context, *args):
        for field_name in form.data.getFields():
            try:
                field = form.data.getField(field_name)
                setattr(context, field.id, field.value)
            except:
                pass


    def retrieve_data(self, form, context, *args):

        data = FormData()

        for field_name in form.data.getFields():

            data.addField(Field(field_name, getattr(context, field_name, None)))

        return data



    @property
    def data(self):

        return {'name': self.__data__['filename'],
                'data': self.__data__['data'].open('r').read()}


    @data.setter
    def data(self, value):
        """ override the setter """

        f = self.__data__['data'].open('w')
        f.write(value['data'])
        # todo: do something with the size?
        f.close()
        # store the filename in attribute storage
        self.__data__['filename'] = value['name']
        self._p_changed = 1

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
        return {'name': self.__data__['filename'],
                'data': blob.open('r').read()}

    @property
    def thumbnail(self):

        """ return the thumbnail, or lazy create it when not present
        yet """

        key = '__cached_blob_thumbnail'
        if not hasattr(self, key):
            self._store_resized_image(key, resize_image(self.data))
        return self._get_resized_image(key)

    def get_size(self, size=(800, 600)):

        """ return the resized image, or lazy create it when not present
        yet """

        key = '_cached_blob_%s_%s' % size
        if not hasattr(self, key):
            self._store_resized_image(key, resize_image(self.data, size))
        return self._get_resized_image(key)

    @property
    def base_id(self):

        return getattr(self, 'name', 'image')


    @property
    def title(self):

        return getattr(self, 'name', 'image')
