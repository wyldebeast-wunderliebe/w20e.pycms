from base import BaseFolder
from ..blocks.base import BlockContainer


class Folder(BaseFolder):

    """ simple folder """

    add_form = edit_form = "../forms/folder.xml"

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
