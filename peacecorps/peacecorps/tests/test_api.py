from unittest.mock import Mock

from django.test import TestCase

from peacecorps import api
from peacecorps.models import Account, Country, Media, Project


class ProjectDetailTests(TestCase):
    def test_serialize_volunteer(self):
        project = Project(volunteername='B. Smith',
                          volunteerhomestate='ID')
        result = api._serialize_volunteer(project)
        self.assertEqual(result['name'], 'B. Smith')
        self.assertEqual(result['homestate'], 'ID')
        self.assertEqual(result['picture'], None)

        project.volunteerpicture = Media()
        project.volunteerpicture.file = Mock()
        project.volunteerpicture.file.url = 'urlhere'
        result = api._serialize_volunteer(project)
        self.assertEqual(result['name'], 'B. Smith')
        self.assertEqual(result['homestate'], 'ID')
        self.assertEqual(result['picture'], 'urlhere')

    def test_serialize_account(self):
        account = Account()
        project = Project(account=account)

        result = api._serialize_account(project)
        self.assertEqual(result['goal'], None)
        self.assertEqual(result['community_contribution'], None)
        self.assertEqual(result['total_donated'], 0)
        self.assertEqual(result['total_raised'], 0)
        self.assertEqual(result['total_cost'], 0)
        self.assertEqual(result['percent_raised'], 0)
        self.assertEqual(result['percent_community'], 0)
        self.assertEqual(result['remaining'], 0)
        self.assertEqual(result['funded'], False)

        account.goal = 2400
        account.community_contribution = 600
        account.current = 900
        result = api._serialize_account(project)
        self.assertEqual(result['goal'], 2400)
        self.assertEqual(result['community_contribution'], 600)
        self.assertEqual(result['total_donated'], 900)
        self.assertEqual(result['total_raised'], 1500)
        self.assertEqual(result['total_cost'], 3000)
        self.assertEqual(result['percent_raised'], 50)
        self.assertEqual(result['percent_community'], 20)
        self.assertEqual(result['remaining'], 1500)
        self.assertEqual(result['funded'], False)

        account.current = 2400
        result = api._serialize_account(project)
        self.assertEqual(result['total_donated'], 2400)
        self.assertEqual(result['total_raised'], 3000)
        self.assertEqual(result['percent_raised'], 100)
        self.assertEqual(result['remaining'], 0)
        self.assertEqual(result['funded'], True)

    def test_serialize(self):
        country = Country(name='Awesomeland')
        account = Account()
        project = Project(account=account, country=country)
        pd = api.ProjectDetail()

        result = pd.serialize(project)
        self.assertEqual(result['title'], '')
        self.assertEqual(result['tagline'], None)
        self.assertEqual(result['country'], 'Awesomeland')
        self.assertEqual(result['featured_image'], None)

        project.title = 'SomeTitle'
        project.tagline = 'SomeTagline'
        project.featured_image = Media()
        project.featured_image.file = Mock()
        project.featured_image.file.url = 'urlhere'
        result = pd.serialize(project)
        self.assertEqual(result['title'], 'SomeTitle')
        self.assertEqual(result['tagline'], 'SomeTagline')
        self.assertEqual(result['featured_image'], 'urlhere')
