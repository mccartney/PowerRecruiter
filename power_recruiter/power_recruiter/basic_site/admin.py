from django.contrib import admin

from power_recruiter.basic_site.models import Notification, Edge, State
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Edge)
admin.site.register(State)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "days", "state")

admin.site.register(Notification, NotificationAdmin)
