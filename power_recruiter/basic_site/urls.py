from django.conf.urls import patterns, url
from views.index import *

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
)