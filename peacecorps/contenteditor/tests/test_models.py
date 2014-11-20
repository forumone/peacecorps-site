from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from contenteditor import models
from peacecorps.models import Country


class ExtraUserTests(TestCase):
    def test_creation(self):
        user = get_user_model().objects.create_user('bob', password='bob')
        self.assertNotEqual(None, user.extra.password_expires)
        user.delete()
        self.assertEqual(0, len(models.ExtraUserFields.objects.all()))


class SignalTests(TestCase):
    def test_user_logging(self):
        """We should receive a log when a user is created and deleted"""
        with self.assertLogs('peacecorps.users') as logger:
            user = get_user_model().objects.create_user(
                username='bob', email='bob@example.com', password='bob')
        self.assertEqual(1, len(logger.output))
        self.assertTrue('bob (bob@example.com)' in logger.output[0])
        self.assertTrue('created' in logger.output[0])

        with self.assertLogs('peacecorps.users') as logger:
            user.delete()
        self.assertEqual(1, len(logger.output))
        self.assertTrue('bob (bob@example.com)' in logger.output[0])
        self.assertTrue('deleted' in logger.output[0])

    def test_admin_edits(self):
        """When models are created, edited, and deleted, a logging entry
        should be made"""
        user = get_user_model().objects.create_user(
            username='bob', email='bob@example.com', password='bob')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username='bob', password='bob')
        with self.assertLogs('peacecorps.admin_edit') as logger:
            self.client.post('/admin/peacecorps/country/add/',
                             data={'code': 'XYZ', 'name': 'Mystery'})
        country = Country.objects.get(code='XYZ')
        self.assertEqual(1, len(logger.output))
        self.assertTrue('bob (bob@example.com)' in logger.output[0])
        self.assertTrue('added' in logger.output[0])
        self.assertTrue('Mystery' in logger.output[0])
        self.assertTrue(str(country.id) in logger.output[0])

        with self.assertLogs('peacecorps.admin_edit') as logger:
            self.client.post('/admin/peacecorps/country/%d/' % country.id,
                             data={'code': 'XYZ', 'name': 'CountryName'})
        self.assertEqual(1, len(logger.output))
        self.assertTrue('bob (bob@example.com)' in logger.output[0])
        self.assertTrue('edited' in logger.output[0])
        self.assertTrue('CountryName' in logger.output[0])
        self.assertTrue(str(country.id) in logger.output[0])

        with self.assertLogs('peacecorps.admin_edit') as logger:
            self.client.post(
                '/admin/peacecorps/country/%d/delete/' % country.id,
                data={'post': 'yes', 'submit': "Yes, I'm sure"})
        self.assertEqual(1, len(logger.output))
        self.assertTrue('bob (bob@example.com)' in logger.output[0])
        self.assertTrue('deleted' in logger.output[0])
        self.assertTrue('CountryName' in logger.output[0])
        self.assertTrue(str(country.id) in logger.output[0])
        user.delete()


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
