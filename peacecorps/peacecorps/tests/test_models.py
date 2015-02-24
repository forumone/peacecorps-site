import json
import os
import shutil
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase

from peacecorps import models


class AccountTest(TestCase):
    def _make_donation(self, acct, amount):
        donation = models.Donation.objects.create(account=acct, amount=amount)
        donation.save()
        return donation

    def test_funded(self):
        account = models.Account()
        self.assertFalse(account.funded())
        account.current = 100
        self.assertFalse(account.funded())
        account.goal = 101
        self.assertFalse(account.funded())
        account.goal = 100
        self.assertTrue(account.funded())
        account.goal = 99
        self.assertTrue(account.funded())

    def test_track_total_donated(self):
        """Use fake data to verify that account totals are being
        kept up-to-date"""
        acc1 = models.Account.objects.create(
            name='Account1', code='112-358', current=150)
        self._make_donation(acc1, 75)
        self._make_donation(acc1, 100)
        self._make_donation(acc1, 1)

        self.assertEqual(326, acc1.total_donated())
        acc1.delete()

    def test_dynamic_total(self):
        """We expect dynamic total to be on any retrieved objects. We expect
        calling `total_donated` to also set this field"""
        acc1 = models.Account.objects.create(
            name='Account1', code='112-358', current=150)

        self._make_donation(acc1, 75)
        self._make_donation(acc1, 100)
        self._make_donation(acc1, 1)
        self.assertFalse(hasattr(acc1, 'dynamic_total'))

        acc1_retrieved = models.Account.objects.get(code='112-358')
        self.assertTrue(hasattr(acc1_retrieved, 'dynamic_total'))
        self.assertEqual(acc1_retrieved.dynamic_total, 176)

        self.assertEqual(acc1.total_donated(), 326)
        self.assertTrue(hasattr(acc1, 'dynamic_total'))
        self.assertEqual(acc1.dynamic_total, 176)

        acc1.delete()

    def test_percent_raised(self):
        account = models.Account()
        account.donations = []
        account.current = 30
        account.community_contribution = 10
        account.goal = 70
        self.assertEqual(50, account.percent_raised())  # 40/80
        account.current += 20
        self.assertEqual(75, account.percent_raised())  # 60/80

    def test_percent_community(self):
        account = models.Account()
        account.community_contribution = 80
        account.goal = 80
        self.assertEqual(50, account.percent_community())   # 80/160
        account.community_contribution = 100
        self.assertEqual(55.56, account.percent_community())    # 100/180


class ProjectTests(TestCase):
    fixtures = ['countries.yaml']

    def test_published(self):
        """Publish is not set by default"""
        account = models.Account.objects.create(name='Acc', code='ACC')
        models.Project.objects.all().delete()
        proj = models.Project.objects.create(
            country=models.Country.objects.get(name='Mexico'),
            account=account)
        self.assertFalse(proj.published)
        self.assertEqual(1, len(models.Project.objects.all()))
        self.assertEqual(0, len(models.Project.published_objects.all()))

        proj.published = True
        proj.save()
        self.assertEqual(1, len(models.Project.objects.all()))
        self.assertEqual(1, len(models.Project.published_objects.all()))

        proj.delete()
        account.delete()

    def test_slug_collision(self):
        """Project slug should be derived from title, yet unique"""
        account1 = models.Account.objects.create(name='Acc', code='ACC')
        account2 = models.Account.objects.create(name='Acc2', code='ACC2')
        country = models.Country.objects.get(name='Mexico')
        proj1 = models.Project.objects.create(
            title='Project', country=country, account=account1)
        proj2 = models.Project.objects.create(
            title='Project', country=country, account=account2)
        self.assertEqual(proj1.slug, 'project')
        self.assertEqual(proj2.slug, 'project' + str(proj1.id))
        account1.delete()
        account2.delete()

    def test_issue(self):
        """Should retrieve the *first* (alpha) issue associated with this
        issue, by passing through any campaigns"""
        paccount = models.Account.objects.create(name='P', code='PROJ')
        c1account = models.Account.objects.create(name='C1', code='CPN1')
        c2account = models.Account.objects.create(name='C2', code='CPN2')
        country = models.Country.objects.get(name='Mexico')
        issue1 = models.Issue.objects.create(name='AAA')
        issue2 = models.Issue.objects.create(name='BBB')
        issue3 = models.Issue.objects.create(name='CCC')

        proj = models.Project.objects.create(
            title='Project', country=country, account=paccount)
        self.assertEqual(proj.issue(check_cache=False), None)

        cpn1 = models.Campaign.objects.create(
            name='Campaign1', account=c1account,
            campaigntype=models.Campaign.SECTOR)
        cpn2 = models.Campaign.objects.create(
            name='Campaign2', account=c2account,
            campaigntype=models.Campaign.SECTOR)
        proj.campaigns.add(cpn1)
        self.assertEqual(proj.issue(check_cache=False), None)

        issue3.campaigns.add(cpn1)
        self.assertEqual(proj.issue(check_cache=False), issue3)

        issue2.campaigns.add(cpn1)
        self.assertEqual(proj.issue(check_cache=False), issue2)

        proj.campaigns.add(cpn2)
        self.assertEqual(proj.issue(check_cache=False), issue2)

        issue1.campaigns.add(cpn2)
        self.assertEqual(proj.issue(check_cache=False), issue1)

        models.Issue.objects.all().delete()     # cascades
        models.Account.objects.all().delete()

    def test_issue_icon_color(self):
        issue = models.Issue()
        self.assertEqual("", issue.icon_color("blue"))
        mock_file = Mock()
        mock_file.name = 'somepath/to/icons/area/filename.bob.sVG'
        issue.icon = mock_file
        self.assertEqual('somepath/to/icons/area/filename.bob-blue.sVG',
                         issue.icon_color('blue'))

    def test_abstract_html(self):
        """The first *text* paragraph should be returned (and rendered) if no
        abstract is present. Otherwise, the abstract should be returned."""
        description = {'data': [{'type': 'other'}]}
        proj = models.Project(description=json.dumps(description))
        self.assertTrue('<p></p>' in proj.abstract_html())

        description['data'].append({'type': 'text',
                                    'data': {'text': 'He*llo*'}})
        proj.description = json.dumps(description)
        self.assertTrue('He<em>llo</em>' in proj.abstract_html())

        # Should also trim the result
        description['data'][1]['data']['text'] = "hello " * 1000
        proj.description = json.dumps(description)
        # The text has been shortened, but markup's been added
        self.assertTrue(len(proj.abstract_html()) < 400)
        self.assertTrue("..." in proj.abstract_html())
        self.assertTrue(proj.slug in proj.abstract_html())
        self.assertFalse("read more" in proj.abstract_html(read_more_link=False))

        proj.abstract = "This is the abstract"
        self.assertTrue("This is the abstract" in proj.abstract_html())

    def test_volunteer_statename(self):
        """This should expand to the whole state name, if we know the
        translation. If not, we should return the text unmodified"""
        proj = models.Project()
        self.assertEqual(proj.volunteer_statename(), None)
        proj.volunteerhomestate = 'RR'
        self.assertEqual(proj.volunteer_statename(), 'RR')
        proj.volunteerhomestate = 'IN'
        self.assertEqual(proj.volunteer_statename(), 'Indiana')


class FAQTests(TestCase):
    def test_slug(self):
        q = 'Very Long Question Because Want Slug Greater Than Fifty'
        faq = models.FAQ.objects.create(question=' '.join([q, q, q]))
        self.assertEqual(len(faq.slug), 50)
        faq.delete()


class ImageSaveTests(TestCase):
    @patch.object(models.Media, 'save')
    def test_no_two_save_calls(self, media_save):
        description = json.dumps({"data": [
            {"type": "image508",
             "data": {"file": {"path": "pathpath"},
                      "image_description": "descdesc",
                      "image_title": "titletitle"}}]})
        models.imagesave(description)
        self.assertEqual(1, media_save.call_count)


class MediaTests(TestCase):
    @patch('peacecorps.models.default_storage')
    def test_reset_seek(self, default_storage):
        """The file head position should get reset. We can confirm this by
        saving the same media model twice."""
        imagepath = 'pc_logo.png'
        # Copy a dummy png
        shutil.copyfile(os.path.join('peacecorps', 'static', 'peacecorps',
                                     'img', imagepath),
                        os.path.join(settings.MEDIA_ROOT, imagepath))
        thisimage = models.Media(
            title="PC Logo",
            file=imagepath,
            mediatype=models.Media.IMAGE,
            description="The Peace Corps Logo.",)
        thisimage.save()
        try:
            thisimage.save()
        except OSError:
            self.fail("Should *not* receive a IOError when saving twice")

    @patch('peacecorps.models.default_storage')
    def test_resize_saved(self, default_storage):
        """Verify that the default storage is getting all three images"""
        imagepath = 'pc_logo.png'
        # Copy a dummy png
        shutil.copyfile(os.path.join('peacecorps', 'static', 'peacecorps',
                                     'img', imagepath),
                        os.path.join(settings.MEDIA_ROOT, imagepath))
        thisimage = models.Media(
            title="PC Logo",
            file=imagepath,
            mediatype=models.Media.IMAGE,
            description="The Peace Corps Logo.",)
        thisimage.save()
        self.assertTrue(default_storage.save.call_count, 4)
        os.remove(os.path.join(settings.MEDIA_ROOT, imagepath))
