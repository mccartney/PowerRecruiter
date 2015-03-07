from django.shortcuts import render

from power_recruiter.basic_site.workflow import WORKFLOW_STATES
from power_recruiter.basic_site.models import Notification
from power_recruiter.candidate.models import Person

def index(request):

    notifications_num = 0
    for person in Person.objects.all():
        notifications_num += len(person.get_person_notifications())

    return render(request, "main.html", {
        "states": WORKFLOW_STATES,
        "notifications": notifications_num
    })
