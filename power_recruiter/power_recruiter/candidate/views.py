import json
from django.http import HttpResponse
import power_recruiter.candidate.models
from django.shortcuts import redirect


def get_attachment(request, id):
    att = power_recruiter.candidate.models.Attachment.objects.get(pk=id)
    return redirect(att.file.url)


def remove_attachment(request, id):
    return HttpResponse(json.dumps(1), content_type="application.json")


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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_candidate(request):
    args = json.loads(request.POST['args'])['args']
    names = args[0].split(' ')
    first_name = names[0]
    last_name = names[len(names) - 1]
    power_recruiter.candidate.models.Person.objects.create_person(first_name, last_name)
    return HttpResponse(200, content_type="plain/text")