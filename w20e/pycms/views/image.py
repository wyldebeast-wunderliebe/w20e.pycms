

from .base import AdminView
from pyramid.response import FileResponse, Response
import mimetypes
from w20e.forms.submission.blob import TheBlob
from ZODB.blob import Blob


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

        if isinstance(blob, str):
            # hmm. no blob image.. (should probably never happen)
            response = Response(blob, content_type=mimeType)
            etag = len(blob)

        elif isinstance(blob, TheBlob):

            # get file path.. don't know the proper way to do this..
            # but open() sort of works..
            opened_file = blob.open_blob('r')

            etag = blob._blob._p_mtime

            response = FileResponse(opened_file.name, self.request,
                    content_type=mimeType)

        elif isinstance(blob, Blob):

            # get file path.. don't know the proper way to do this..
            # but open() sort of works..
            opened_file = blob.open('r')

            etag = blob._p_mtime

            response = FileResponse(opened_file.name, self.request,
                    content_type=mimeType)

        else:
            raise ValueError("Not a valid image type")

        # set response caching headers..

        response.etag = str(etag)
        response.cache_expires = (3600 * 24 * 7)

        return response

    def __call__(self):

        return self._return_file_response(self.context._data_['data'])

    def thumbnail(self):

        return self._return_file_response(self.context.thumbnail)


class ImageAdminView(AdminView):

    pass
