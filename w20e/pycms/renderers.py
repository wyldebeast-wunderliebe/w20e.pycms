import hashlib
import mimetypes
from pyramid.response import FileResponse


class JSRenderer:

    """ Render content as iCal """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        m = hashlib.md5()
        m.update(value)
        etag = m.hexdigest()

        system['request'].response.content_type = 'text/javascript'

        system['request'].response.conditional_response = True
        system['request'].response.etag = etag
        system['request'].response.vary = 'Accept-Encoding'

        # should we set the expires explicitly?
        # don't set expires to 0, or no-cache will be set, and it will
        # disable the conditional get (304 response with etag)
        system['request'].response.cache_expires = 300

        return value


class CSSRenderer:

    """ Render content as iCal """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        m = hashlib.md5()
        m.update(value)
        etag = m.hexdigest()

        system['request'].response.content_type = 'text/css'

        system['request'].response.conditional_response = True
        system['request'].response.etag = etag
        system['request'].response.vary = 'Accept-Encoding'

        # should we set the expires explicitly?
        # don't set expires to 0, or no-cache will be set, and it will
        # disable the conditional get (304 response with etag)
        system['request'].response.cache_expires = 300

        return value


class PNGRenderer:

    """ Render content as image """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        etag = str(len(value['data']))

        filename = value['name']

        mimeType = "image/png"

        try:
            guessed = mimetypes.guess_type(filename, strict=False)[0]
            if guessed:
                mimeType = guessed
        except:
            pass

        system['request'].response.content_type = mimeType

        system['request'].response.conditional_response = True
        system['request'].response.etag = etag
        system['request'].response.vary = 'Accept-Encoding'

        # should we set the expires explicitly?
        # don't set expires to 0, or no-cache will be set, and it will
        # disable the conditional get (304 response with etag)
        system['request'].response.cache_expires = 300

        return value['data']


class FileRenderer:

    """ Render content as file (disposition attachment) """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        filename = value['name']
        mimeType = mimetypes.guess_type(filename, strict=False)[0] or ''
        system['request'].response.content_type = mimeType
        system['request'].response.content_disposition = \
            'attachment; filename="{0}"'.format(value['name'])

        return value['data']


class AjaxRenderer:

    """ Return value as is """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        """ Value should be a dict with name and data as keys """

        system['request'].response.headerlist = [
            ('Cache-Control', 'no-cache'),
            ('Pragma', 'No-Cache')]

        system['request'].response.content_type = 'text/xml'

        return value


class XMLRenderer:

    """ Return value as is """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        """ Value should be a dict with name and data as keys """

        system['request'].response.headerlist = [
            ('Cache-Control', 'no-cache'),
            ('Pragma', 'No-Cache')]

        system['request'].response.content_type = 'text/xml'

        if isinstance(value, unicode):
            value = value.encode('utf-8')

        return value


class HTMLRenderer:

    """ Return value as is """

    def __init__(self, info):

        pass

    def __call__(self, value, system):

        """ Value should be a dict with name and data as keys """

        system['request'].response.headerlist = [
            ('Cache-Control', 'no-cache'),
            ('Pragma', 'No-Cache')]

        system['request'].response.content_type = 'text/html'

        return value
