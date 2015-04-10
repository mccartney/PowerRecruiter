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
