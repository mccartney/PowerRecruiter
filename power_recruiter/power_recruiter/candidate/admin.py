from django.contrib import admin

from power_recruiter.candidate.models import Person, Attachment, \
    Contact, Role


admin.site.register(Person)
admin.site.register(Attachment)
admin.site.register(Contact)
admin.site.register(Role)
