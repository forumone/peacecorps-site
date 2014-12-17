from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone


class ExpirationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('joe', password='joe')
        self.user.is_staff = True
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_can_access(self):
        """If a password is not expired, the user can access admin pages"""
        client = Client()
        client.login(username=self.user.username, password=self.user.username)
        resp = client.get('/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_cannot_access(self):
        """If a password has expired, the user cannot access most pages"""
        self.user.extra.password_expires = timezone.now()
        self.user.extra.save()
        client = Client()
        client.login(username=self.user.username, password=self.user.username)
        resp = client.get('/admin/')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/admin/password_change/' in resp['LOCATION'])

    def test_access_whitelist(self):
        """If a password has expired, certain pages in a whitelist are still
        accessible"""
        with self.settings(PASSWORD_EXPIRATION_WHITELIST='/admin/'):
            self.user.extra.password_expires = timezone.now()
            self.user.extra.save()
            client = Client()
            client.login(username=self.user.username,
                         password=self.user.username)
            resp = client.get('/admin/')
            self.assertEqual(resp.status_code, 200)


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('joe', password='joe')
        self.user.is_staff = True
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_extra_checks(self):
        """Verify that the password change page checks our extra
        requirements"""
        client = Client()
        client.login(username=self.user.username, password=self.user.username)
        resp = client.post('/admin/password_change/',
                           data={'old_password': self.user.username,
                                 'new_password1': 'q*9x=^2hg&v7u?u9tg?u',
                                 'new_password2': 'q*9x=^2hg&v7u?u9tg?u'})
        self.assertContains(resp, 'errorlist')
        # Add an uppercase letter
        resp = client.post('/admin/password_change/',
                           data={'old_password': self.user.username,
                                 'new_password1': 'q*9x=^2Hg&v7u?u9tg?u',
                                 'new_password2': 'q*9x=^2Hg&v7u?u9tg?u'})
        self.assertEqual(resp.status_code, 302)
