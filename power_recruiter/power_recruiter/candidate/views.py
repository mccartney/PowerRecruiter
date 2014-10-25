import json
from django.http import HttpResponse
import power_recruiter.candidate.models
from django.shortcuts import redirect


<<<<<<< HEAD
def get_attachment(request, id):
=======
def attachment(request, id):
>>>>>>> 9d32bb4f40502b77301e82cbe33cbc437a0ad1c8
    att = power_recruiter.candidate.models.Attachment.objects.get(pk=id)
    return redirect(att.file.url)


<<<<<<< HEAD
def remove_attachment(request, id):
    return HttpResponse(json.dumps(1), content_type="application.json")


=======
>>>>>>> 9d32bb4f40502b77301e82cbe33cbc437a0ad1c8
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