import mimetypes
#from ..blobfile import File
from w20e.hitman.models.base import BaseContent
from ZODB.blob import Blob
from w20e.forms.formdata import FormData
from w20e.forms.data.field import Field


class File(BaseContent):

    """ File model """

    add_form = edit_form = "../forms/file.xml"


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

    @property
    def base_id(self):

        return getattr(self, 'name', 'file')


    @property
    def title(self):

        return getattr(self, 'name', 'file')
