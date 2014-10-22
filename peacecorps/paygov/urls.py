from django.conf.urls import patterns, url

from paygov.views import data, results


urlpatterns = patterns(
    '',
    url(r'^data/?$', data, name='data'),
    url(r'^results/?$', results, name='results')
    # url(r'^settlement/?$', settlement)
)
