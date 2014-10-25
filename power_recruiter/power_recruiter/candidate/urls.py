from django.conf.urls import patterns, url

from power_recruiter.candidate.views import attachment, candidate_json


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'attachment/(?P<id>\d+)$', attachment, name='attachment')
)