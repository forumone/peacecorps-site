from django.contrib.auth.models import User
from django.test import TestCase

from contenteditor import models


class ExtraUserTests(TestCase):
    def test_creation(self):
        user = User.objects.create_user('bob', password='bob')
        self.assertNotEqual(None, user.extra.password_expires)
        user.delete()
        self.assertEqual(0, len(models.ExtraUserFields.objects.all()))
