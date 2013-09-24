from zope.interface import implements
from base import BaseFolder
from interfaces import IFolder


class Folder(BaseFolder):

    implements(IFolder)

    """ simple folder """

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
