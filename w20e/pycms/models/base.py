from pyramid.threadlocal import get_current_registry
from w20e.hitman.models.base import BaseFolder as HitmanBaseFolder
from w20e.hitman.models.base import BaseContent as HitmanBaseContent
from w20e.pycms.security import ISecure
from w20e.pycms.ctypes import ICTypes


class PyCMSMixin:

    @property
    def __acl__(self):

        try:
            return get_current_registry().getAdapter(self, ISecure).__acl__
        except:
            return []


class BaseContent(HitmanBaseContent, PyCMSMixin):

    allowed_content_types = []
        

class BaseFolder(HitmanBaseFolder, PyCMSMixin):

    @property
    def allowed_content_types(self):

        ctypes = get_current_registry().getUtility(ICTypes)

        return ctypes.get_ctype_info(
            self.content_type).get("subtypes", "").split(",")
