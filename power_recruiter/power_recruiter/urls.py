from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from power_recruiter.basic_site.admin import admin_auto_login_site

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_auto_login_site.get_urls(), namespace='admin')),
    url(r'', include('power_recruiter.basic_site.urls')),
    url(r'^candidate/', include('power_recruiter.candidate.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
