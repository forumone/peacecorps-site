from django.conf.urls import patterns, url

from paygov.views import data


urlpatterns = patterns(
    '',
    url(r'^data/?$', data, name='data')
    # url(r'^results/?$', results)
    # url(r'^settlement/?$', settlement)
)
