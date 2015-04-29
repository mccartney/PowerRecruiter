from django.shortcuts import render
from django.conf import settings

from power_recruiter.candidate.models import Person, State


def create_pie_chart_context():
    return {
        "static_js": settings.STATIC_JS_PATH,
        'spices': [{
            'num': len(Person.objects.filter(state=state)),
            'name': state.get_name()
        } for state in State.objects.all()]
    }


def pie_chart(request):
    return render(request, "pie_chart.html", create_pie_chart_context())
