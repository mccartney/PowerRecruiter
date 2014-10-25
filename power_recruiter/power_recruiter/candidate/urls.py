from django.conf.urls import patterns, url

from power_recruiter.candidate.views.candidate_json import candidate_json
from power_recruiter.candidate.views.attachment import attachment


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'attachment/id=(?P<id>\d+)$', attachment, name='attachment')
)