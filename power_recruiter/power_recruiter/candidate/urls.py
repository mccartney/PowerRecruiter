from django.conf.urls import patterns, url

from power_recruiter.candidate.views.candidate_json import candidate_json


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
)