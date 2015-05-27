from django.conf.urls import patterns, url

from power_recruiter.candidate.views import get_attachment, \
    remove_attachment, candidate_json, add_candidate, change_state, \
    upload_attachment, caveats_upload, change_name, remove_person, \
    get_conflicts, resolve_conflicts, add_candidate_from_app


urlpatterns = patterns(
    '',
    url(r'^$', candidate_json, name='json'),
    url(r'^attachment/upload/$', upload_attachment, name='upload'),
    url(r'^attachment/get/(?P<attachment_id>\d+)$', get_attachment,
        name='get_attachment'),
    url(r'^attachment/remove/$', remove_attachment,
        name='remove_attachment'),
    url(r'^add_from_app', add_candidate_from_app),
    url(r'^add', add_candidate),
    url(r'^remove/$', remove_person, name='remove_person'),
    url(r'^change_state/$', change_state, name='change_state'),
    url(r'^change_name/$', change_name, name='change_name'),
    url(r'^caveats/upload/$', caveats_upload, name='caveats_upload'),
    url(r'^get_conflicts/$', get_conflicts),
    url(r'^resolve_conflicts/$', resolve_conflicts),
)
