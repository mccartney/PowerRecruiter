from django.shortcuts import render
from power_recruiter.candidate.models import RecruitmentState

def index(request):
    states = RecruitmentState.objects.all()
    return render(request, "main.html", {"states": states})
