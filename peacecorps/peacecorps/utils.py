from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.conf import settings
import pdb

def image_sizes(file_):

    def resize(image, size, ext, filename):
        image.thumbnail(size, Image.ANTIALIAS)

        path = settings.MEDIA_ROOT + settings.SIRTREVOR_UPLOAD_PATH

        image.save(path+filename+'-'+ext+'.'+ image.format.lower(),
            image.format)
        return None

    filename = file_.name.split('.')[0]

    lg = (1200, 1200)
    md = (900, 900)
    sm = (500, 500)
    thm = (300, 300)

    im = Image.open(file_)
    resize(im, lg, 'lg', filename)
    resize(im, md, 'md', filename)
    resize(im, sm, 'sm', filename)
    resize(im, thm, 'thm', filename)

    return file_
    # SimpleUploadedFile(file_.name, im, content_type=im.format)

