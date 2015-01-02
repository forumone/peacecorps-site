import os
import shutil
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from peacecorps.models import Media


class ResizeTests(TestCase):
    @patch('peacecorps.models.default_storage')
    def test_resize_saved(self, default_storage):
        """Verify that the default storage is getting all three images"""
        imagepath = 'pc_logo.png'
        # Copy a dummy png
        shutil.copyfile(os.path.join('peacecorps', 'static', 'peacecorps',
                                     'img', imagepath),
                        os.path.join(settings.MEDIA_ROOT, imagepath))
        thisimage = Media(
            title="PC Logo",
            file=imagepath,
            mediatype=Media.IMAGE,
            description="The Peace Corps Logo.",)
        thisimage.save()
        self.assertTrue(default_storage.save.call_count, 4)
        os.remove(os.path.join(settings.MEDIA_ROOT, imagepath))
