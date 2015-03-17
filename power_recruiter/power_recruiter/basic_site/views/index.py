from django.shortcuts import render

from power_recruiter.basic_site.workflow import get_states_dict
from power_recruiter.candidate.models import Person


def index(request):

    notifications_num = 0
    for person in Person.objects.all():
        notifications_num += len(person.get_person_notifications())

    states = get_states_dict()
    return render(request, "main.html", {
        "states": states,
        "notifications": notifications_num
    })
