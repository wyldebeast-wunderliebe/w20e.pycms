from base import BaseFolder


class Folder(BaseFolder):

    """ simple folder """

    @property
    def base_id(self):

        return self.__data__['name']

    @property
    def title(self):

        return self.__data__['name']
