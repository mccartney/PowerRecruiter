from django.conf.urls import patterns, url

from power_recruiter.basic_site.views.index import index


urlpatterns = patterns(
    '',
    url(r'^$', index, name='home'),
    #url(r'^.*$', handler404, name='notFound'),
)
