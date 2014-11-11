from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from contenteditor.admin import (
    StrictUserCreationForm, StrictAdminPasswordChangeForm)


class StrictUserCreationTest(TestCase):
    def test_blank(self):
        """ Check to ensure the password cannot be blank."""
        form_data = {
            'username': 'testuser',
            'password1': '',
            'password2': ''
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_match(self):
        """ Check to ensure the passwords match."""
        form_data = {
            'username': 'testuser',
            'password1': 'q*A9x=^2hg&v7u?u9tg?u',
            'password2': 'A=r7-%=K?K@B^!9Q8=C+'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_uppercase(self):
        """ Check to ensure the password contains an uppercase letter."""
        form_data = {
            'username': 'testuser',
            'password1': 'q*9x=^2hg&v7u?u9tg?u',
            'password2': 'q*9x=^2hg&v7u?u9tg?u'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_lowercase(self):
        """ Check to ensure the password contains a lowercase letter."""
        form_data = {
            'username': 'testuser',
            'password1': 'A=R7-%=K?K@B^!9Q8=C+',
            'password2': 'A=R7-%=K?K@B^!9Q8=C+'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_number(self):
        """ Check to ensure the password contains a number."""
        form_data = {
            'username': 'testuser',
            'password1': 'CDr=cpz&Z&a!cuP-nAQe',
            'password2': 'CDr=cpz&Z&a!cuP-nAQe'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_specialchar(self):
        """ Check to ensure the password contains a special character."""
        form_data = {
            'username': 'testuser',
            'password1': 'vNzwXpzKJyTshvHsuULn',
            'password2': 'vNzwXpzKJyTshvHsuULn'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_length(self):
        """ Check to ensure the password is 20 characters long."""
        form_data = {
            'username': 'testuser',
            'password1': 'c897B$eH@',
            'password2': 'c897B$eH@'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_passwordsuccess(self):
        """ Check to ensure the password, when proper, is successful."""
        form_data = {
            'username': 'testuser',
            'password1': '2$n5[]$nnA5Y}2}}^gba',
            'password2': '2$n5[]$nnA5Y}2}}^gba'
        }
        form = StrictUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class StrictAdminPasswordChangeFormTest(TestCase):
    def setUp(self):
        username = 'testuser'
        pwd = 'q*A9x=^2hg&v7u?u9tg?u'

        self.u = User.objects.create_user(username, '', pwd)
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.save()
        self.pwd = pwd

        self.assertTrue(
            self.client.login(username=username, password=pwd),
            "Logging in user %s, pwd %s failed." % (username, pwd))

    def tearDown(self):
        self.u.delete()

    def test_blank(self):
        """ Check to ensure the password cannot be blank."""
        form_data = {
            'password1': '',
            'password2': ''
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_match(self):
        """ Check to ensure the passwords match."""
        form_data = {
            'password1': 'r*A9x=^2hg&v7u?u9tg?u',
            'password2': 'A=r7-%=K?K@B^!9Q8=C+'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_uppercase(self):
        """ Check to ensure the password contains an uppercase letter."""
        form_data = {
            'password1': 'q*9x=^2hg&v7u?u9tg?u',
            'password2': 'q*9x=^2hg&v7u?u9tg?u'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_lowercase(self):
        """ Check to ensure the password contains a lowercase letter."""
        form_data = {
            'password1': 'A=R7-%=K?K@B^!9Q8=C+',
            'password2': 'A=R7-%=K?K@B^!9Q8=C+'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_number(self):
        """ Check to ensure the password contains a number."""
        form_data = {
            'password1': 'CDr=cpz&Z&a!cuP-nAQe',
            'password2': 'CDr=cpz&Z&a!cuP-nAQe'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_specialchar(self):
        """ Check to ensure the password contains a special character."""
        form_data = {
            'password1': 'vNzwXpzKJyTshvHsuULn',
            'password2': 'vNzwXpzKJyTshvHsuULn'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_length(self):
        """ Check to ensure the password is 20 characters long."""
        form_data = {
            'password1': 'c897B$eH@',
            'password2': 'c897B$eH@'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_passwordsuccess(self):
        """ Check to ensure the password, when proper, is successful. Verify
        that the password expiration field gets updated"""
        old_time = timezone.now()
        self.u.extra.password_expires = old_time
        form_data = {
            'password1': '2$n5[]$nnA5Y}2}}^gba',
            'password2': '2$n5[]$nnA5Y}2}}^gba'
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertTrue(form.is_valid())
        form.save()
        new_time = User.objects.get(
            username=self.u.username).extra.password_expires
        self.assertTrue(new_time > old_time)

    def test_new_password(self):
        """ Password must be different than the current """
        form_data = {
            'password1': self.pwd,
            'password2': self.pwd
        }
        form = StrictAdminPasswordChangeForm(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())
