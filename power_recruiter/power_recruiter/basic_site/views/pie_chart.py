from django.shortcuts import render
from power_recruiter.basic_site.workflow import WORKFLOW_STATES
from power_recruiter.candidate.models import Person

def pie_chart(request):
    context = {
        'spices': [{
            'num': len(Person.objects.filter(state=k)),
            'name': v.get_name()
        } for k, v in WORKFLOW_STATES.iteritems()]
    }
    return render(request, "pie_chart.html", context)