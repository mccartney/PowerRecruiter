from django.shortcuts import render

from power_recruiter.candidate.models import Person, State


def pie_chart(request):
    context = {
        'spices': [{
            'num': len(Person.objects.filter(state=state)),
            'name': state.get_name()
        } for state in State.objects.all()]
    }
    return render(request, "pie_chart.html", context)
