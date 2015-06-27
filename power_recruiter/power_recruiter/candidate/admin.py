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
from django import forms
from power_recruiter.candidate.models import Person, Attachment, \
    ResolvedConflict
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
