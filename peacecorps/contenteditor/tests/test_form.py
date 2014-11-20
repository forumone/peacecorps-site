from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from contenteditor.forms import (
    StrictAdminPasswordChangeForm, StrictPasswordChangeForm,
    StrictUserCreationForm)


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


class AbstractPasswordChange(object):
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

    def form_data(self, password1, password2=None):
        """Generate fields for the password form submission. We're generally
        testing password constraints, so include a shorthand for duplicating
        password1"""
        form_data = {'old_password': self.pwd}
        if password2 is None:
            password2 = password1
        form_data[self.password_field + '1'] = password1
        form_data[self.password_field + '2'] = password2
        return form_data

    def test_blank(self):
        """ Check to ensure the password cannot be blank."""
        form_data = self.form_data('')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_match(self):
        """ Check to ensure the passwords match."""
        form_data = self.form_data('r*A9x=^2hg&v7u?u9tg?u',
                                   'A=r7-%=K?K@B^!9Q8=C+')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_uppercase(self):
        """ Check to ensure the password contains an uppercase letter."""
        form_data = self.form_data('q*9x=^2hg&v7u?u9tg?u')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_lowercase(self):
        """ Check to ensure the password contains a lowercase letter."""
        form_data = self.form_data('A=R7-%=K?K@B^!9Q8=C+')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_number(self):
        """ Check to ensure the password contains a number."""
        form_data = self.form_data('CDr=cpz&Z&a!cuP-nAQe')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_specialchar(self):
        """ Check to ensure the password contains a special character."""
        form_data = self.form_data('vNzwXpzKJyTshvHsuULn')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_length(self):
        """ Check to ensure the password is 20 characters long."""
        form_data = self.form_data('c897B$eH@')
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())

    def test_passwordsuccess(self):
        """ Check to ensure the password, when proper, is successful. Verify
        that the password expiration field gets updated"""
        old_time = timezone.now()
        self.u.extra.password_expires = old_time
        form_data = self.form_data('2$n5[]$nnA5Y}2}}^gba')
        form = self.form(data=form_data, user=self.u)
        self.assertTrue(form.is_valid())
        form.save()
        new_time = User.objects.get(
            username=self.u.username).extra.password_expires
        self.assertTrue(new_time > old_time)

    def test_new_password(self):
        """ Password must be different than the current """
        form_data = self.form_data(self.pwd)
        form = self.form(data=form_data, user=self.u)
        self.assertFalse(form.is_valid())


class StrictAdminPasswordChangeFormTest(AbstractPasswordChange, TestCase):
    password_field = 'password'
    form = StrictAdminPasswordChangeForm


class StrictPasswordChangeFormTest(AbstractPasswordChange, TestCase):
    password_field = 'new_password'
    form = StrictPasswordChangeForm


class LoggingAuthenticationFormTest(TestCase):
    def test_success(self):
        user = User.objects.create_user('LOgin', 'bob@example.com', 'passpass')
        user.is_staff = True
        user.save()
        with self.assertLogs("peacecorps.login") as logger:
            response = self.client.post(
                '/admin/login/', data={'username': user.username,
                                       'password': 'passpass'})
            self.assertEqual(302, response.status_code)
        self.assertEqual(1, len(logger.output))
        self.assertTrue('LOgin' in logger.output[0])
        self.assertTrue('success' in logger.output[0])
        user.delete()

    def test_failure(self):
        """Test both a missing password and an incorrect password"""
        user = User.objects.create_user('LOgin', 'bob@example.com', 'passpass')
        user.is_staff = True
        user.save()
        with self.assertLogs("peacecorps.login") as logger:
            response = self.client.post(
                '/admin/login/', data={'username': user.username,
                                       'password': ''})
            self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(logger.output))
        self.assertTrue('LOgin' in logger.output[0])
        self.assertTrue('Fail' in logger.output[0])

        with self.assertLogs("peacecorps.login") as logger:
            response = self.client.post(
                '/admin/login/', data={'username': user.username,
                                       'password': 'wrong'})
            self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(logger.output))
        self.assertTrue('LOgin' in logger.output[0])
        self.assertTrue('Fail' in logger.output[0])
        user.delete()
