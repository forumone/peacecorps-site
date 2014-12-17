import os
from unittest.mock import patch

from django.test import TestCase

from contenteditor import imagesizing


class ResizeTests(TestCase):
    @patch('contenteditor.imagesizing.default_storage')
    def test_resize_saved(self, default_storage):
        """Verify that the default storage is getting all three images"""
        path = os.path.join('peacecorps', 'static', 'peacecorps', 'img',
                            'pc_logo.png')
        original = open(path, 'rb')
        imagesizing.resize(original)
        self.assertTrue(default_storage.save.call_count, 4)
