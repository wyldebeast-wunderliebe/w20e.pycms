from base import BaseFolder
from ..blocks.base import BlockContainer
from pyramid.threadlocal import get_current_registry
from ..ctypes import ICTypes


class Folder(BaseFolder):

    """ simple folder """

    add_form = edit_form = "../forms/folder.xml"

    @property
    def allowed_content_types(self):

        ctypes = get_current_registry().getUtility(ICTypes)

        return ctypes.get_ctype_info(
            self.content_type).get("subtypes", "").split(",")

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
