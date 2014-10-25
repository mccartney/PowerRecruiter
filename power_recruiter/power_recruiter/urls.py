from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('power_recruiter.basic_site.urls')),
    url(r'candidate', include('power_recruiter.candidate.urls'))
)

