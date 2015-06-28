"""
Power Recruiter - a browser-based FSM-centered database application profiled for IT recruiters
Copyright (C) 2015 Krzysztof Fudali, Andrzej Jackowski, Cezary Kosko, Filip Ochnik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from power_recruiter.basic_site.admin import admin_auto_login_site


handler404 = 'power_recruiter.basic_site.views.handler404.handler404'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_auto_login_site.get_urls(),
        namespace='admin')),
    url(r'', include('power_recruiter.basic_site.urls')),
    url(r'^candidate/', include('power_recruiter.candidate.urls'))
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
