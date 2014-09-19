from django.conf.urls import patterns, include, url
from django.contrib import admin

from peacecorps.views import donation_payment_us

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^donations/contribute/us$',
        donation_payment_us, name='donations_contribute'),
)
