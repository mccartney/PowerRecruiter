from django.contrib import admin

from power_recruiter.candidate.models import Person, Attachment, \
    Communication, Source, Role


admin.site.register(Person)
admin.site.register(Attachment)
admin.site.register(Communication)
admin.site.register(Source)
admin.site.register(Role)
