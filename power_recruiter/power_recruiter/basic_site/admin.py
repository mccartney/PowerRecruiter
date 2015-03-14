from django.contrib import admin

from power_recruiter.basic_site.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "days", "state")

admin.site.register(Notification, NotificationAdmin)
