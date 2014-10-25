from django.conf.urls import patterns, url
from power_recruiter.candidate.views import get_attachment, candidate_json, remove_attachment
from power_recruiter.candidate.views import attachment, candidate_json


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'attachment/get/(?P<id>\d+)$', get_attachment, name='get_attachment'),
    url(r'attachment/remove/(?P<id>\d+)$', remove_attachment, name='remove_attachment'),
    url(r'attachment/(?P<id>\d+)$', attachment, name='attachment')

)