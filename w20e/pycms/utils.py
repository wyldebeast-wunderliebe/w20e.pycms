import sys
import os
from PIL import Image as PILImage
from ZODB.blob import Blob
from StringIO import StringIO
import time
import random
import hashlib
from pyramid.security import has_permission as base_has_permission
from w20e.forms.submission.blob import TheBlob


THUMBNAIL_SIZE = 128, 128
KEY_LENGTH = 24


def has_permission(permission, context, request):

    """ Cache permission in request """

    key = 'permission_%s_%s' % (permission, context.dottedpath)

    if not key in request.environ:
        request.environ[key] = base_has_permission(permission, context, request)
        
    return request.environ[key]


def resize_image(data, size=THUMBNAIL_SIZE):

    """ generate the thumbnail, and store it as an attribute """

    # TODO: blob handling needs some streamlining..
    if isinstance(data['data'], Blob):
        pil_img = PILImage.open(data['data'].open())
    elif isinstance(data['data'], TheBlob):
        image_data = StringIO(data['data'].get())
        pil_img = PILImage.open(image_data)
    else:
        image_data = StringIO(data['data'])
        pil_img = PILImage.open(image_data)

    pil_img.thumbnail(size, PILImage.ANTIALIAS)

    thumb_buf = StringIO()
    pil_img.save(thumb_buf, format='PNG')

    return {'name': data['name'], 'data': thumb_buf.getvalue()}


def generate_id(prefix="", length=KEY_LENGTH):

    """ Generate unique registration key """

    t1 = time.time()
    time.sleep(random.random())
    t2 = time.time()
    base = hashlib.md5(str(t1 + t2))

    return prefix + base.hexdigest()[:length]


def package_home(globals_dict):
    __name__=globals_dict['__name__']
    m=sys.modules[__name__]
    if hasattr(m,'__path__'):
        r=m.__path__[0]
    elif "." in __name__:
        r=sys.modules[__name__[:__name__.rfind('.')]].__path__[0]
    else:
        r=__name__
    return os.path.abspath(r)


def path_to_object(path, root, path_sep="/"):

    """ Given a path, return the object from the hierarchy """

    path = path.split(path_sep)[1:]
    path = [p for p in path if p]

    if not len(path):
        return root

    obj = None
    parent = root

    for elt in path[:-1]:
        parent = parent.get(elt, None)
        if parent is None:
            break

    if parent is not None:
        obj = parent.get(path[-1], None)

    return obj


def object_to_path(obj, path_sep="/", as_list=False):

    """ Give an object, return the path """

    path = [obj._id]

    _root = obj

    while getattr(_root, "__parent__", None) is not None:
        _root = _root.__parent__
        path.append(_root.id)

    path.reverse()

    if as_list:
        return path[1:]
    else:
        value = path_sep.join([''] + path[1:])
        if not value.startswith(path_sep):
            value = path_sep + value
        return value
