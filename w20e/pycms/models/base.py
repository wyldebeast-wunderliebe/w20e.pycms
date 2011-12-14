from pyramid.threadlocal import get_current_registry
from w20e.hitman.models.base import BaseFolder as HitmanBaseFolder
from w20e.hitman.models.base import BaseContent as HitmanBaseContent
from w20e.pycms.security import ISecure


class PyCMSMixin:

    @property
    def __acl__(self):

        try:
            return get_current_registry().getAdapter(self, ISecure).__acl__
        except:
            return []
    

class BaseContent(HitmanBaseContent, PyCMSMixin):

    pass

class BaseFolder(HitmanBaseFolder, PyCMSMixin):

    pass
