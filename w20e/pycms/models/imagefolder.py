from folder import Folder


class ImageFolder(Folder):

    """ simple folder that may only contain images """

    add_form = edit_form = "../forms/imagefolder.xml"

    def __init__(self, content_id):

        Folder.__init__(self, content_id)
