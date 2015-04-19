from django.shortcuts import render
from django.conf import settings
from power_recruiter.candidate.models import Person, State


def index(request):

    notifications_num = 0
    for person in Person.objects.all():
        notifications_num += len(person.get_person_notifications())
    states = State.objects.all()
    k = len(states)
    return render(request, "main.html", {
        "states": dict(zip(range(k), states)),
        "notifications": notifications_num,
        "static_js": settings.STATIC_JS_PATH
    })
