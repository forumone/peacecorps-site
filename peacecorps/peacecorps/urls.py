from django.conf.urls import patterns, include, url
from django.contrib import admin

from peacecorps.views import donation_payment
from peacecorps.views import donation_payment_review

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^donations/contribute/?$',
        donation_payment, name='donations_payment'),
    url(
        r'^donations/review/?$',
        donation_payment_review, name='donations_review'),
)
