import os
from base import BaseContent
from ..utils import package_home


current_folder = package_home(globals())


class File(BaseContent):

    """ File model """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'file.xml')

    @property
    def base_id(self):

        return self.__data__['data']['name']

    @property
    def title(self):

        return self.__data__['name']
