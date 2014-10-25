import json

from django.http import HttpResponse
from django.core import serializers

from power_recruiter.candidate.models \
    import Person, Attachment, Communication, InternetLocation, RecruitmentState, Role


def candidate_json(request):
    persons = Person.objects.all()
    resp = []
    for p in persons:
        resp.append({
            'id' : p.pk,
            'candidate' : p.first_name + ' ' + p.last_name,
            'cos' : 'guwno',
        })
    return HttpResponse(json.dumps(resp), content_type="application/json")