from django.contrib import admin
from power_recruiter.candidate.models \
    import Person, Attachment, Communication, Source, RecruitmentState, Role

# Register your models here.
admin.site.register(Person)
admin.site.register(Attachment)
admin.site.register(Communication)
admin.site.register(Source)
admin.site.register(RecruitmentState)
admin.site.register(Role)