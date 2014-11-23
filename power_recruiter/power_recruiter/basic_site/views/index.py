from django.shortcuts import render

from power_recruiter.basic_site.workflow import WORKFLOW_STATES


def index(request):
    return render(request, "main.html", {"states": WORKFLOW_STATES})
