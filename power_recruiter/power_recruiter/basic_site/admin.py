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

from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.admin import AdminSite
from power_recruiter.basic_site.models import Notification, Edge, State
from django.contrib.auth import login as auth_login


class AutoLoginAdminSite(AdminSite):

    def login(self, request, extra_context=None):
        user = authenticate(username='root', password='root')
        auth_login(request, user)
        return super(AutoLoginAdminSite, self).login(request)

    def get_urls(self):
        urls = super(AutoLoginAdminSite, self).get_urls()
        return urls

admin_auto_login_site = AutoLoginAdminSite()
admin_auto_login_site.register(State)


class NotificationAdmin(admin.ModelAdmin):
    fields = ("message", "days", "state")
    list_display = ("message", "days", "get_state_view")

admin_auto_login_site.register(Notification, NotificationAdmin)


class EdgeAdmin(admin.ModelAdmin):
    list_display = ("get_view", )

admin_auto_login_site.register(Edge, EdgeAdmin)
