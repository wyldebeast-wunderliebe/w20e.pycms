from pyramid.url import resource_url
from ..models.image import Image
from w20e.hitman.models.exceptions import UniqueConstraint


def _remove_prefix(string, prefix):
    return string[len(prefix):] if string.startswith(prefix) else string


class TinyBrowser:
    """ browse and upload files from TinyMCE """

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def _get_images_folder(self):
        """ return the images folder """
        images_folder = self.context.root['images']
        return images_folder


    def browse_images(self):
        """ browse images """
        images_folder = self._get_images_folder()
        images = images_folder.list_content(content_type='image')
        result = []
        root_url = self.request.application_url
        for i in images:
            i_url = resource_url(i, self.request)
            i_url = _remove_prefix(i_url, root_url)
            i_thumb_url = resource_url(i, self.request) + "thumbnail"
            i_thumb_url = _remove_prefix(i_thumb_url, root_url)
            result.append({'file': i.id, 'url': i_url, 'thumb_url': i_thumb_url})
        return result

    def upload_image(self):
        """ upload an image """
        status = 0
        message = "ok"

        try:
            images_folder = self._get_images_folder()
            uploaded_image = self.request.params.get('tiny-upload-image')
            img_id = self.context.generate_content_id(uploaded_image.filename)
            img_data = {
                    'name': uploaded_image.filename,
                    'data': {
                        'name': uploaded_image.filename,
                        'data': uploaded_image.value}
                    }
            img = Image(img_id, img_data)
            images_folder.add_content(img)
        except UniqueConstraint:
            status = 1
            message = "An image with this ID already exists"
        except Exception as err:
            status = 9
            message = "Unexpected error occured: %s " % err

        return {'status': status, 'message': message}
