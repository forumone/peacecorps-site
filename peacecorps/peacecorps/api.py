import json

from django.core.urlresolvers import reverse
from restless.models import serialize
from restless.modelviews import DetailEndpoint

from peacecorps.models import Account, Project


def _serialize_volunteer(project):
    """Pull out fields related to a volunteer into a dict"""
    if project.volunteerpicture:
        picture = project.volunteerpicture.url
    else:
        picture = None
    return {'name': project.volunteername,
            'homestate': project.volunteerhomestate,
            'picture': picture}


def _serialize_account(project):
    """Generate several useful fields related to a project's account"""
    account = project.account
    return {'goal': account.goal,
            'community_contribution': account.community_contribution,
            'total_donated': account.total_donated(),
            'total_raised': account.total_raised(),
            'total_cost': account.total_cost(),
            'percent_raised': account.percent_raised(),
            'percent_community': account.percent_community(),
            'funded': account.funded(),
            'remaining': account.remaining()}


def _serialize_overflow(project):
    """Overflow url for a project; path depends on the account type"""
    if project.overflow:
        if project.overflow.category == Account.PROJECT:
            view_name = 'donate project'
        else:
            view_name = 'donate campaign'
        return reverse(
            view_name,
            kwargs={'slug': project.overflow.project_or_fund().slug})
    return None


def _serialize_description(project):
    """The description content is stored as JSON. Kind of silly to deserialize
    and then serialize, but oh well"""
    try:
        return json.loads(project.description)
    except ValueError:
        return None


class ProjectDetail(DetailEndpoint):
    model = Project     # @todo - reduce number of queries
    lookup_field = 'slug'

    def serialize(self, obj):
        """The idealized project is a bit different than the DB model"""
        return serialize(
            obj,
            fields=(
                'title',
                'tagline',
                ('description', _serialize_description),
                ('volunteer', _serialize_volunteer),
                ('country', lambda o: o.country.name),
                ('account', _serialize_account),
                ('overflow', _serialize_overflow),
                ('featured_image',
                    lambda o: o.featured_image.url if o.featured_image
                    else None),
            ),

        )
