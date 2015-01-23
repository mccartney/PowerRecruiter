from django.conf.urls import patterns, url

from power_recruiter.candidate.views import get_attachment, \
    remove_attachment, candidate_json, add_candidate, change_state, \
    upload, caveats_upload, change_name, remove_person


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'^attachment/get/(?P<attachment_id>\d+)$', get_attachment,
        name='get_attachment'),
    url(r'^attachment/remove/$', remove_attachment,
        name='remove_attachment'),
    url(r'^add', add_candidate),
    url(r'^remove/$', remove_person, name='remove_person'),
    url(r'^attachment/upload/$', upload, name='upload'),
    url(r'^change_state/$', change_state, name='change_state'),
    url(r'^change_name/$', change_name, name='change_name'),
    url(r'^attachment/upload/$', upload, name='upload'),
    url(r'^caveats/upload/$', caveats_upload, name='caveats_upload'),
)
