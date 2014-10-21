from django.conf.urls import patterns, include, url
from django.contrib import admin

from views.index import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'power_recruiter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', index)
)
