from folder import BaseFolder


class ImageFolder(BaseFolder):

    """ simple folder that may only contain images """

    add_form = edit_form = "../forms/imagefolder.xml"

    def __init__(self, content_id):

        BaseFolder.__init__(self, content_id)
