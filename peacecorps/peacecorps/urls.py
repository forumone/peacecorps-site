from django.apps import apps
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

from peacecorps import api, views
from peacecorps.cache import midterm_cache, shortterm_cache

_slug = r'(?P<slug>[a-zA-Z0-9_-]+)'

apipatterns = patterns(
    '',
    url(r'^project/' + _slug + r'/$',
        shortterm_cache(api.ProjectDetail.as_view()), name='project_detail'),
    url(r'^project/' + _slug + r'/payment/$',
        api.ProjectDonation.as_view(), name='project_payment'),
    url(r'^fund/' + _slug + r'/payment/$',
        api.FundDonation.as_view(), name='fund_payment'),
)


urlpatterns = patterns(
    '',
    url(r'^donate/$', midterm_cache(views.donate_landing),
        name='donate landing'),
    url(r'^donate/projects-funds/$',
        midterm_cache(views.donate_projects_funds),
        name='donate projects funds'),
    url(r'^donate/projects-funds/memorial/$',
        midterm_cache(views.memorial_funds), name='donate memorial funds'),
    url(r'^donate/faq/$', midterm_cache(views.FAQs.as_view()),
        name='donate faqs'),

    url(r'^donate/fund/' + _slug + r'/$',
        midterm_cache(views.fund_detail), name='donate campaign'),
    # not cached so the values are up-to-date
    url(r'^donate/fund/' + _slug + r'/payment/$',
        views.campaign_form, name='campaign form'),
    url(r'^donate/fund/' + _slug + r'/success/$',
        views.CampaignReturn.as_view(
            template_name='donations/campaign_success.jinja'),
        name='campaign success'),
    url(r'^donate/fund/' + _slug + r'/failure/$',
        views.failure, {'redirect_to': 'donate campaign'},
        name='campaign failure'),

    url(r'^donate/project/' + _slug + r'/$',
        midterm_cache(views.donate_project), name='donate project'),
    # not cached so the values are up-to-date
    url(r'^donate/project/' + _slug + r'/payment/$',
        views.project_form, name='project form'),
    url(r'^donate/project/' + _slug + r'/success/$',
        views.ProjectReturn.as_view(
            template_name='donations/project_success.jinja'),
        name='project success'),
    url(r'^donate/project/' + _slug + r'/failure/$',
        views.failure, {'redirect_to': 'donate project'},
        name='project failure'),

    url(r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")),

    url(r'^api/', include(apipatterns, namespace='api')),

    url(r'^donate/api/v1/projects/',
        views.ProjectListAPI.as_view(),
        name='projects api'),

    url(r'^donate/api/v1/campaigns/country',
        views.CountryCampaignListAPI.as_view(),
        name='campaigns api'),
)


handler404 = views.four_oh_four


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('', url(r'^404/$', handler404))

if apps.is_installed('paygov'):
    urlpatterns += patterns(
        '', url(r'^callback/', include('paygov.urls', namespace='paygov')))

if apps.is_installed('contenteditor'):
    urlpatterns += patterns(
        '',
        url(r'^admin/', include('contenteditor.urls')),
        url(r'^admin/sirtrevor/', include('sirtrevor.urls')))
