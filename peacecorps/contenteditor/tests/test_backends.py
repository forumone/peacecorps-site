from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import Client, TestCase

from contenteditor.models import Editor
from peacecorps.models import Media


class EditorBackendTests(TestCase):
    def test_request_user(self):
        """Verify that the request user is an 'Editor' """
        user = User.objects.create_user('tim', password='tim')
        client = Client()
        client.login(username=user.username, password=user.username)
        request = HttpRequest()
        request.session = client.session
        user = get_user(request)
        self.assertTrue(isinstance(user, Editor))
        user.delete()


class LoggingStorageTests(TestCase):
    def test_events_logged(self):
        storage_str = 'django.core.files.storage.FileSystemStorage'
        with self.settings(LOGGED_FILE_STORAGE=storage_str):
            with self.assertLogs('peacecorps.files') as logger:
                media = Media.objects.create(
                    title="Example", description="Example Content",
                    file=SimpleUploadedFile('fILENAMe.txt', b'contents'))
            self.assertEqual(1, len(logger.output))
            self.assertTrue('Saved' in logger.output[0])
            self.assertTrue('fILENAMe.txt' in logger.output[0])
            with self.assertLogs('peacecorps.files') as logger:
                # Note that django does not delete the file when the model is
                # destroyed
                media.file.storage.delete('fILENAMe.txt')
                media.delete()
            self.assertEqual(1, len(logger.output))
            self.assertTrue('Deleted' in logger.output[0])
            self.assertTrue('fILENAMe.txt' in logger.output[0])
