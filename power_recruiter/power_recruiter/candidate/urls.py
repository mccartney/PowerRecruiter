from django.conf.urls import patterns, url

from power_recruiter.candidate.views import get_attachment, \
    remove_attachment, candidate_json, add_candidate, stats, upload, caveatsUpload

urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'attachment/get/(?P<id>\d+)$', get_attachment, name='get_attachment'),
    url(r'attachment/remove/(?P<id>\d+)$', remove_attachment,
        name='remove_attachment'),
    url(r'add', add_candidate),
    url(r'stats$', stats, name='stats'),
    url(r'attachment/upload/$', upload, name='upload'),
    url(r'caveats/upload/', caveatsUpload, name='caveatsUpload')
)
