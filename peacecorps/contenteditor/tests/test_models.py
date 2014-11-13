from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from contenteditor import models


class ExtraUserTests(TestCase):
    def test_creation(self):
        user = get_user_model().objects.create_user('bob', password='bob')
        self.assertNotEqual(None, user.extra.password_expires)
        user.delete()
        self.assertEqual(0, len(models.ExtraUserFields.objects.all()))


class EditorTests(TestCase):
    def test_blank(self):
        """ Check to ensure the password cannot be blank."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser', 'password': ''})

    def test_uppercase(self):
        """ Check to ensure the password contains an uppercase letter."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser',
                           'password': 'q*9x=^2hg&v7u?u9tg?u'})

    def test_lowercase(self):
        """ Check to ensure the password contains a lowercase letter."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser',
                           'password': 'A=R7-%=K?K@B^!9Q8=C+'})

    def test_number(self):
        """ Check to ensure the password contains a number."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser',
                           'password': 'CDr=cpz&Z&a!cuP-nAQe'})

    def test_specialchar(self):
        """ Check to ensure the password contains a special character."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser',
                           'password': 'vNzwXpzKJyTshvHsuULn'})

    def test_length(self):
        """ Check to ensure the password is 20 characters long."""
        self.assertRaises(ValidationError, models.Editor.objects.create_user,
                          {'username': 'testuser',
                           'password': 'c897B$eH@'})
