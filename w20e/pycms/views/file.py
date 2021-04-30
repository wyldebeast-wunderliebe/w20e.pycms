from __future__ import absolute_import
from builtins import str
from builtins import object
from .base import AdminView
from pyramid.response import FileResponse, Response
from w20e.forms.submission.blob import TheBlob
import mimetypes
from ZODB.blob import Blob as Blob
from slugify import slugify


class FileView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def _return_file_response(self, value):

        blob = value['data']

        filename = value['name']
        mimeType = "application/octet-stream"

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

            # Can't use FileResponse like this because file might be zipped

            # get file path.. don't know the proper way to do this..
            # but open() sort of works..
            #opened_file = blob.open_blob('r')
            etag = blob._blob._p_mtime
            #response = FileResponse(opened_file.name, self.request,
            #                        content_type=mimeType)

            response = Response(blob.get(), content_type=mimeType)

        elif isinstance(blob, Blob):

            # get file path.. don't know the proper way to do this..
            # but open() sort of works..
            opened_file = blob.open('r')

            etag = blob._p_mtime

            response = FileResponse(opened_file.name, self.request,
                                    content_type=mimeType)

        else:
            raise ValueError("Not a valid file type")

        # set response caching headers..

        response.etag = str(etag)
        response.cache_expires = (3600 * 24 * 7)

        name = slugify(value['name'], lowercase=False)
        response.content_disposition = u'attachment; filename="{0}"'.format(
            name)

        return response

    def __call__(self):

        # caching headers should not be set here hardcoded,
        # but it'll have to do for now..
        return self._return_file_response(self.context.__data__['data'])

    def download_file(self):
        """ This assumes the file is stored as an attribute on the context """

        assert 'file_field' in self.request.params, "something's rotten"
        assert 'form_id' in self.request.params, "something's rotten"
        file_field = self.request.params['file_field']
        form_id = self.request.params['form_id']
        # check of the default form is what we expect it to be..
        # TODO: have some sort of default loading other forms on a context
        if self.context.__form__(self.request).id != form_id:
            raise Exception("Only downloads from default form is supported "
                            "at this moment.")
        return self._return_file_response(self.context.__data__[file_field])


class FileAdminView(AdminView):

    pass
