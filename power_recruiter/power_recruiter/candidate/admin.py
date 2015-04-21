from django.contrib import admin
from django import forms
from power_recruiter.candidate.models import Person, Attachment, ResolvedConflict
from power_recruiter.basic_site.admin import admin_auto_login_site

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
    fields = (
        "photo_url",
        "first_name",
        "last_name",
        "state",
        "linkedin",
        "goldenline",
        "email",
    )

    list_display = (
        "first_name",
        "last_name",
        "get_state_view",
        "linkedin",
        "goldenline",
        "email",
    )

    form = PersonForm

class ResolvedConflictAdmin(admin.ModelAdmin):
    fields = ("person_one", "person_two")
    list_display = ("name_first_with_id", "name_second_with_id")


admin_auto_login_site.register(Person, PersonAdmin)
admin_auto_login_site.register(Attachment)
admin_auto_login_site.register(ResolvedConflict, ResolvedConflictAdmin)
