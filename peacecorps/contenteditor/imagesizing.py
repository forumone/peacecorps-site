import os
import tempfile

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image


# We'll be mutating an image, so scale from larger to smaller
SIZES = (('lg', 1200, 1200), ('md', 900, 900), ('sm', 500, 500),
         ('thm', 300, 300))


def resize(original_file):
    """When an image has been uploaded, resize it to thumbnails, etc."""

    filename = original_file.name.split('.')[0]

    image = Image.open(original_file)
    for ext, width, height in SIZES:
        with tempfile.TemporaryFile() as buffer_file:
            image.thumbnail((width, height), Image.ANTIALIAS)
            path = os.path.join(
                settings.SIRTREVOR_UPLOAD_PATH,
                filename + '-' + ext + '.' + image.format.lower())
            image.save(buffer_file, image.format.lower())
            default_storage.save(path, buffer_file)

    return original_file
