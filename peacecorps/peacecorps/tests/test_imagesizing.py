from unittest.mock import patch

from django.test import TestCase

from django.core.files.storage import default_storage
from peacecorps.models import Media
from django.conf import settings


class ResizeTests(TestCase):
    @patch('peacecorps.models.default_storage')
    def test_resize_saved(self, default_storage):
        """Verify that the default storage is getting all three images"""
        imagepath = 'pc_logo.png'
        thisimage = Media(
            title="PC Logo",
            file=imagepath,
            mediatype=Media.IMAGE,
            description="The Peace Corps Logo.",)
        thisimage.save()
        self.assertTrue(default_storage.save.call_count, 4)
