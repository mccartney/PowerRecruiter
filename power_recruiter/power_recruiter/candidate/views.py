import json
from django.http import HttpResponse
import power_recruiter.candidate.models
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


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
        source = p.source.name
        if 'http' in p.source.name:
            source = '<a href=' + p.source.name + '>'
            if 'linkedin' in p.source.name:
                source += '<img style="width:50px; height:50px" src="http://www.socialtalent.co/wp-content/uploads/2014/07/LinkedIn_logo_initials.png">' + '</a>'
            else:
                if 'goldenline' in p.source.name:
                     source += 'goldenLine' + '</a>'
                else:
                    source += 'link' + '</a>'
        resp.append({
            'id': p.pk,
            'candidate_name': p.first_name + ' ' + p.last_name,
            'source': source,
            'type': p.role.name,
            'comm': p.comm.name,
            'attachments': attachments,
            'caveats': p.caveats,
        })
    return HttpResponse(json.dumps(resp), content_type="application/json")

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)

@csrf_exempt
def add_candidate(request):
    args = []
    for i in ['0', '1', '2']:
        args.append(request.POST['args['+i+']'])
    names = args[0].split(' ')
    first_name = names[0]
    last_name = names[len(names) - 1]
    power_recruiter.candidate.models.Person.objects.create_person(first_name, last_name, args[2])
    return HttpResponse(200, content_type="plain/text")