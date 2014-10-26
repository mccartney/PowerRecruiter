import json
import logging
import sys

from django.http import HttpResponse, HttpResponseRedirect
import power_recruiter.candidate.models
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from power_recruiter.candidate.models import Attachment, Person, RecruitmentState
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
import power_recruiter.candidate.models

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Attachment

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
                'display_name': str(a),
                'pk': a.pk
            } for a in power_recruiter.candidate.models.Attachment.objects.filter(person_id=p.pk)
        ]
        source = p.source.name
        if 'http' in p.source.name:
            source = '<a href=' + p.source.name + '>'
            if 'linkedin' in p.source.name:
                source += '<img style="width:38px; height:38px" ' \
                          'src="http://www.socialtalent.co/wp-content/' \
                          'uploads/2014/07/LinkedIn_logo_initials.png">'
            else:
                if 'goldenline' in p.source.name:
                    source += 'goldenLine'
                else:
                    source += 'link'
            source += '</a>'
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


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = Attachment(person = Person.objects.get(id=request.POST['person']), file = request.FILES['file'])
            new_file.save()

            return HttpResponseRedirect(reverse('upload'))
    else:
        form = UploadFileForm()

    data = {'form': form}
    return render_to_response('main.html', data, context_instance=RequestContext(request))

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
    power_recruiter.candidate.models.Person.objects.create_person(
        first_name,
        last_name,
        args[2]
    )
    return HttpResponse(200, content_type="plain/text")


def stats(request):
    states = RecruitmentState.objects.all()
    context = {
        'spices' : [
            {'num' : len(Person.objects.filter(state = s.pk)), 'name' : s.name} for s in states
        ]
    }
    return render(request, "stats.html", context)