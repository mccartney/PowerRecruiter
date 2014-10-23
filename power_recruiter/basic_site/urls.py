from django.conf.urls import patterns, url
from views.index import index
from views.handler404 import handler404

urlpatterns = patterns(
    '',
    url(r'^$', index, name='home'),
    #url(r'^.*$', handler404, name='notFound'),
)
