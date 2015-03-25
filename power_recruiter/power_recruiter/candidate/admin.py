from django.contrib import admin
from django import forms

from power_recruiter.candidate.models import Person, Attachment, Role


class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields["photo_url"].required = False
        self.fields["linkedin"].required = False
        self.fields["goldenline"].required = False
        self.fields["email"].required = False

    class Meta:
        model = Person
        exclude = ("current_state_started",)


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "state",
        "linkedin",
        "goldenline",
        "email"
    )
    form = PersonForm

admin.site.register(Person, PersonAdmin)


admin.site.register(Attachment)
admin.site.register(Role)
