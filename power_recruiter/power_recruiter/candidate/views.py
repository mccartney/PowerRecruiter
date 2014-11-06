import json
import logging
import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from power_recruiter.candidate.models import Attachment, Person, \
    RecruitmentState


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


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Attachment


def get_attachment(request, attachment_id):
    attachment = Attachment.objects.get(pk=attachment_id)
    return redirect(attachment.file.url)


def remove_attachment(request, attachment_id):
    return HttpResponse(json.dumps(1), content_type="application.json")


def candidate_json(request):
    # TODO: this view needs to be fixed ASAP, it's a mess

    persons = Person.objects.all()

    if request.GET.get('Awaiting contact', 0):
        persons = persons.exclude(state_id=1)
    if request.GET.get('Contact rejected', 0):
        persons = persons.exclude(state_id=2)
    if request.GET.get('Awaiting meeting', 0):
        persons = persons.exclude(state_id=3)
    if request.GET.get('Rejected', 0):
        persons = persons.exclude(state_id=4)
    if request.GET.get('Hired', 0):
        persons = persons.exclude(state_id=5)

    resp = []
    for p in persons:
        attachments = [
            {
                'display_name': str(a),
                'pk': a.pk
            } for a in Attachment.objects.filter(person_id=p.pk)
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
        state = ''
        if p.state_id in [1, 3]:
            state += '<a href="#up" id="upButton' + str(p.pk) + '">' \
                     '<img src="/static/img/bolt.png">' \
                     '</a>' \
                     '<script>$("#upButton' + str(p.pk) + \
                     '").click(function(){' \
                     '$.get( "candidate/up/' + str(p.pk) + '", function() {'\
                     'reloadData();' \
                     '});' \
                     '});</script>'\
                     + p.state.name + \
                     '<a href="#down" id="downButton' + str(p.pk) + '">'\
                     '<img src="/static/img/boltdown.png">' \
                     '</a>' \
                     '<script>$("#downButton' + str(p.pk) + \
                     '").click(function(){' \
                     '$.get( "candidate/down/' + str(p.pk) + \
                     '", function() {' \
                     'reloadData();' \
                     '});' \
                     '});</script>'
        else:
            if "Hired" in p.state.name:
                state = "<span style='color: #419E16'>" + p.state.name + \
                        "</span>"
            else:
                state = "<span style='color: #F00'>" + p.state.name + "</span>"
        resp.append({
            'id': p.pk,
            'candidate_name': p.first_name + ' ' + p.last_name,
            'source': source,
            'state': state,
            'comm': p.comm.name,
            'attachments': attachments,
            'caveats': p.caveats,
        })
    return HttpResponse(json.dumps(resp), content_type="application/json")


@require_POST
@csrf_exempt
def caveats_upload(request):
    person = Person.objects.get(id=request.POST['id'])
    person.caveats = request.POST['caveats']
    person.save()
    return HttpResponseRedirect(reverse('caveats_upload'))


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            person = Person.objects.get(id=request.POST['person'])
            uploaded_file = request.FILES['file']
            new_file = Attachment(person=person, file=uploaded_file)
            new_file.save()
            return HttpResponseRedirect(reverse('upload'))
    else:
        form = UploadFileForm()
    data = {'form': form}
    return render_to_response(
        'main.html',
        data,
        context_instance=RequestContext(request)
    )


def up(request, candidate_id):
    person = Person.objects.get(id=candidate_id)
    person.state_id += 2
    person.save()
    return HttpResponse(200, content_type="plain/text")


def down(request, candidate_id):
    person = Person.objects.get(id=candidate_id)
    person.state_id += 1
    person.save()
    return HttpResponse(200, content_type="plain/text")


@csrf_exempt
def add_candidate(request):
    args = []
    for i in xrange(3):
        args.append(request.POST['args[%d]' % i])
    names = args[0].split(' ')
    first_name = names[0]
    last_name = names[-1]
    if Person.objects.filter(first_name=first_name, last_name=last_name).exists():
        person = Person.objects.filter(first_name=first_name, last_name=last_name).first()
        return HttpResponse(status=418, content_type="plain/text", content=person.state)
    else:
        Person.objects.create_person(
            first_name,
            last_name,
            args[2]
        )
        return HttpResponse(status=200, content=200, content_type="plain/text")


def stats(request):
    states = RecruitmentState.objects.all()
    context = {
        'spices': [{
            'num': len(Person.objects.filter(state=s.pk)),
            'name': s.name
        } for s in states]
    }
    return render(request, "stats.html", context)
