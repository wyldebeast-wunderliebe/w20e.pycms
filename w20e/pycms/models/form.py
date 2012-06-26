import os
from base import BaseContent
from ..utils import package_home


current_folder = package_home(globals())


class Form(BaseContent):

    """ Generic Form """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'form.xml')

    def __init__(self, content_id):

        BaseContent.__init__(self, content_id)

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
