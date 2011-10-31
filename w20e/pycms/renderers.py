import hashlib
import mimetypes


class JSRenderer:

    """ Render content as iCal """

    def __init__(self, info):

        pass


    def __call__(self, value, system):

        m = hashlib.md5()
        m.update(value)
        etag = m.hexdigest()

        system['request'].response.content_type = 'text/javascript'
        system['request'].response.headerlist = [('ETag', etag),
                                                 ('Vary', 'Accept-Encoding')]
        system['request'].response.cache_expires = (3600 * 24 * 7)

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
        system['request'].response.etag = etag
        system['request'].response.cache_expires = (3600 * 24 * 7)

        return value


class PNGRenderer:

    """ Render content as image """

    def __init__(self, info):

        pass


    def __call__(self, value, system):

        etag = len(value['data'])

        filename = value['name']
        mimeType = mimetypes.guess_type(filename, strict=False)[0] or 'image/png'
        system['request'].response.content_type = mimeType
        system['request'].response.etag = etag
        system['request'].response.cache_expires = (3600 * 24 * 7)

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
            ('Cache-Control','no-cache'),
            ('Pragma','No-Cache')]

        system['request'].response.content_type = 'text/xml'

        return value


class XMLRenderer:

    """ Return value as is """

    def __init__(self, info):

        pass


    def __call__(self, value, system):

        """ Value should be a dict with name and data as keys """

        system['request'].response.headerlist = [
            ('Cache-Control','no-cache'),
            ('Pragma','No-Cache')]

        system['request'].response.content_type = 'text/xml'

        return value

