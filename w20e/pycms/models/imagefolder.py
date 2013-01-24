from folder import Folder


class ImageFolder(Folder):

    """ simple folder that may only contain images """

    def __init__(self, content_id, data=None):

        Folder.__init__(self, content_id, data)
