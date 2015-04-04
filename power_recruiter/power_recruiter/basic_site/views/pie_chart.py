from django.shortcuts import render

from power_recruiter.candidate.models import Person, State

def create_pie_chart_context():
    return {
        'spices': [{
            'num': len(Person.objects.filter(state=state)),
            'name': state.get_name()
        } for state in State.objects.all()]
    }

def pie_chart(request):
    return render(request, "pie_chart.html", create_pie_chart_context())
