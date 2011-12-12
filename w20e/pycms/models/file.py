import mimetypes
#from ..blobfile import File
from w20e.hitman.models.base import BaseContent
from ZODB.blob import Blob
from w20e.forms.formdata import FormData
from w20e.forms.data.field import Field


class File(BaseContent):

    """ File model """

    add_form = edit_form = "../forms/file.xml"

    @property
    def base_id(self):

        return self.__data__['data']['name']

    @property
    def title(self):

        return self.__data__['name']
