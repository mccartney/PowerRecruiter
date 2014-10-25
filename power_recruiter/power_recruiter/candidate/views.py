import json
from django.http import HttpResponse
import power_recruiter.candidate.models
from django.shortcuts import redirect


def attachment(request, id):
    att = power_recruiter.candidate.models.Attachment.objects.get(pk=id)
    return redirect(att.file.url)


def candidate_json(request):
    persons = power_recruiter.candidate.models.Person.objects.all()
    resp = []
    for p in persons:
        attachments = [
            {
                'display_name': a.name,
                'pk': a.pk
            } for a in power_recruiter.candidate.models.Attachment.objects.filter(person_id=p.pk)
        ]
        resp.append({
            'id': p.pk,
            'candidate_name': p.first_name + ' ' + p.last_name,
            'source': p.source.name,
            'type': p.role.name,
            'comm': p.comm.name,
            'attachments': attachments,
            'caveats': p.caveats,
        })
    return HttpResponse(json.dumps(resp), content_type="application/json")