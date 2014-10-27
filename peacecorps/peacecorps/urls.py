from django.apps import apps
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from peacecorps.views import donation_failure, donation_payment
from peacecorps.views import donation_success

from peacecorps.views import donate_landing
from peacecorps.views import donate_issue
from peacecorps.views import donate_project
from peacecorps.views import donate_country
from peacecorps.views import donate_countries
from peacecorps.views import donate_memorial
from peacecorps.views import donate_general

urlpatterns = patterns(
    '',
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^donate/?$', donate_landing, name='donate landing'),
    url(r'^donate/issue/(?P<slug>[a-zA-Z0-9_-]*)/?$',
        donate_issue, name='donate issue'),
    url(r'^donate/project/(?P<slug>[a-zA-Z0-9_-]*)/?$',
        donate_project, name='donate project'),
    url(r'^donate/country/(?P<slug>[a-zA-Z0-9_-]*)/?$',
        donate_country, name='donate country'),
    url(r'^donate/countries',
        donate_countries, name='donate countries'),
    url(r'^donate/memorial/(?P<slug>[a-zA-Z0-9_-]*)/?$',
        donate_memorial, name='donate memorial'),
    # this needs to be below other donate urls.
    url(r'^donate/(?P<slug>[a-zA-Z0-9_-]*)/?$',
        donate_general, name='donate general'),
    url(
        r'^donations/contribute/?$',
        donation_payment, name='donations_payment'),
    url(r'^success/?$', donation_success, name='donation success'),
    url(r'^failure/?$', donation_failure, name='donation failure')
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if apps.is_installed('paygov'):
    urlpatterns += patterns(
        '', url(r'^callback/', include('paygov.urls', namespace='paygov')))
