from base import AdminView
from pyramid.response import FileResponse, Response
import mimetypes


class ImageView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def _return_file_response(self, value):

        blob = value['data']
        filename = value['name']
        mimeType = "image/png"

        try:
            guessed = mimetypes.guess_type(filename, strict=False)[0]
            if guessed:
                mimeType = guessed
        except:
            pass

        if isinstance(value['data'], str):
            # hmm. no blob image.. (should probably never happen)
            response = Response(value['data'], content_type=mimeType)
            etag = len(value['data'])

        else:

            # get file path.. don't know the proper way to do this..
            # but open() sort of works..
            opened_file = blob.open('r')

            etag = blob._p_mtime

            response = FileResponse(opened_file.name, self.request,
                    content_type=mimeType)

        # set response caching headers..

        response.etag = str(etag)
        response.cache_expires = (3600 * 24 * 7)

        return response

    def __call__(self):

        return self._return_file_response(self.context.__data__['data'])

    def thumbnail(self):

        return self._return_file_response(self.context.thumbnail)


class ImageAdminView(AdminView):

    pass
