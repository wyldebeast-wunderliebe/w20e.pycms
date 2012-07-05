import os
from base import BaseFolder
from ..utils import package_home


current_folder = package_home(globals())


class Folder(BaseFolder):

    """ simple folder """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'folder.xml')

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
