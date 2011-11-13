from w20e.hitman.models.base import BaseFolder as Base
from ..blocks.base import BlockContainer
from pyramid.threadlocal import get_current_registry
from ..security import ISecure
from ..ctypes import ICTypes


class Folder(Base):

    """ simple folder """

    add_form = edit_form = "../forms/folder.xml"


    def __init__(self, content_id, data={}):

        Base.__init__(self, content_id, data=data)


    @property
    def allowed_content_types(self):

        ctypes = get_current_registry().getUtility(ICTypes)

        return ctypes.get_ctype_info(self.content_type).get("subtypes", "").split(",")


    @property
    def __acl__(self):

        security = None

        try:
            security = get_current_registry().getAdapter(self, ISecure)
        except:
            pass

        if security:
            return security.__acl__
        else:
            return []


    @property
    def base_id(self):

        return self.__data__['name']


    @property
    def title(self):

        return self.__data__['name']


BaseFolder = Folder
