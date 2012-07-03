import os
from folder import Folder
from ..utils import package_home


current_folder = package_home(globals())


class ImageFolder(Folder):

    """ simple folder that may only contain images """

    add_form = edit_form = os.path.join(
            current_folder, '..', 'forms', 'imagefolder.xml')
    def __init__(self, content_id):

        Folder.__init__(self, content_id)
