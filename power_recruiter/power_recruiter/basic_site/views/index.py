from django.shortcuts import render

from power_recruiter.candidate.models import Person, State


def index(request):

    notifications_num = 0
    for person in Person.objects.all():
        notifications_num += len(person.get_person_notifications())

    return render(request, "main.html", {
        "states": State.objects.all(),
        "notifications": notifications_num
    })
