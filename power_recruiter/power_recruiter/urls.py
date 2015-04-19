from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from httpproxy.views import HttpProxy
from power_recruiter.basic_site.admin import admin_auto_login_site


handler404 = 'power_recruiter.basic_site.views.handler404.handler404'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_auto_login_site.get_urls(), namespace='admin')),
    url(r'', include('power_recruiter.basic_site.urls')),
    url(r'^candidate/', include('power_recruiter.candidate.urls'))
)
if settings.REMOTE_DJANGO_STATIC:
    urlpatterns += patterns('', (r'^staticjs/(?P<url>.*)$', HttpProxy.as_view(base_url='http://127.0.0.1:8081/')),)
else:
    urlpatterns += static(settings.STATIC_JS_URL, document_root=settings.STATIC_JS_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
