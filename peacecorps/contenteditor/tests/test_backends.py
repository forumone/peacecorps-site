from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase

from contenteditor.models import Editor


class BackendEditorTests(TestCase):
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
