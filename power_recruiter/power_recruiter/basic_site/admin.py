from django.contrib import admin

from power_recruiter.basic_site.models import Notification, Edge, State
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(State)

class NotificationAdmin(admin.ModelAdmin):
    fields = ("message", "days", "state")
    list_display = ("message", "days", "get_state_view")

admin.site.register(Notification, NotificationAdmin)

class EdgeAdmin(admin.ModelAdmin):
    list_display= ("get_view", )

admin.site.register(Edge, EdgeAdmin)