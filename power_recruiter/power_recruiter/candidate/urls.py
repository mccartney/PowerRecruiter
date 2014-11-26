from django.conf.urls import patterns, url

from power_recruiter.candidate.views import get_attachment, \
    remove_attachment, candidate_json, add_candidate, stats, up, down, \
    upload, caveats_upload

urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'^attachment/get/(?P<attachment_id>\d+)$', get_attachment,
        name='get_attachment'),
    url(r'^attachment/remove/$', remove_attachment,
        name='remove_attachment'),
    url(r'^add', add_candidate),
    url(r'^attachment/upload/$', upload, name='upload'),
    url(r'^up/(?P<candidate_id>\d+)/$', up, name='up'),
    url(r'^down/(?P<candidate_id>\d+)/$', down, name='down'),
    url(r'^stats$', stats, name='stats'),
    url(r'^attachment/upload/$', upload, name='upload'),
    url(r'^caveats/upload/$', caveats_upload, name='caveats_upload')
)
