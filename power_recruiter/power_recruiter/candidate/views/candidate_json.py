import json

from django.http import HttpResponse
from django.core import serializers

from power_recruiter.candidate.models \
    import Person, Attachment, Communication, Source, RecruitmentState, Role


def candidate_json(request):
    persons = Person.objects.all()
    resp = []
    for p in persons:
        attachments = [
            {
                'display_name' : a.name,
                'pk' : a.pk
            } for a in Attachment.objects.filter(person_id = p.pk)
        ]
        resp.append({
            'id' : p.pk,
            'candidate_name' : p.first_name + ' ' + p.last_name,
            'source' : p.source.name,
            'type' : p.role.name,
            'comm' : p.comm.name,
            'attachments' : attachments,
            'caveats' : p.caveats,
        })
    return HttpResponse(json.dumps(resp), content_type="application/json")