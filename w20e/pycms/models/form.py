from base import BaseContent


class Form(BaseContent):

    """ Software project representation """

    add_form = edit_form = "../forms/form.xml"

    def __init__(self, content_id):

        BaseContent.__init__(self, content_id)

    @property
    def base_id(self):

        return self.__data__['name']
