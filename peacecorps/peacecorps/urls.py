from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from peacecorps.views import donation_payment
from peacecorps.views import donation_payment_review

from peacecorps.views import donate_landing
from peacecorps.views import donate_issue
from peacecorps.views import donate_project
from peacecorps.views import donate_country
from peacecorps.views import donate_countries

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
    url(
        r'^donations/contribute/?$',
        donation_payment, name='donations_payment'),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
