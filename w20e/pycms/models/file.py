from base import BaseContent


class File(BaseContent):

    """ File model """

    @property
    def base_id(self):

        return self.__data__['data']['name']

    @property
    def title(self):

        return self.__data__['name']
