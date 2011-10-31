from PIL import Image as PILImage
from StringIO import StringIO
import time,random,hashlib


THUMBNAIL_SIZE = 128, 128
KEY_LENGTH=24


def resize_image(data, size=THUMBNAIL_SIZE):

    """ generate the thumbnail, and store it as an attribute """

    image_data = StringIO(data['data'])
    pil_img = PILImage.open(image_data)
    pil_img.thumbnail(size, PILImage.ANTIALIAS)

    thumb_buf = StringIO()
    pil_img.save(thumb_buf, format= 'PNG')
    return {'name': data['name'], 'data': thumb_buf.getvalue()}



def generate_id(prefix="", length=KEY_LENGTH):

    """ Generate unique registration key """

    t1 = time.time()
    time.sleep(random.random())
    t2 = time.time()
    base = hashlib.md5(str(t1 +t2) )
    return prefix + base.hexdigest()[:length]
