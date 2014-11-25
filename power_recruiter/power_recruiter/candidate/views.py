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

from power_recruiter.candidate.models import Attachment, Person
from power_recruiter.basic_site.workflow import WORKFLOW_STATES, \
    get_next_nodes, get_previous_nodes, node_number_to_name


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

    for k in WORKFLOW_STATES.keys():
        if request.GET.get(str(k), False):
            persons = persons.exclude(state=k)

    resp = []
    for p in persons:
        candidateName = {
            'candidateId': p.pk,
            'candidateName': str(p)
        }

        contact = {
            'candidateId': p.pk,
            'candidateName': str(p),
            'linkedin': p.contact.linkedin,
            'goldenline': p.contact.goldenline,
            'email': p.contact.email
        }

        attachments = [
            {
                'display_name': str(a),
                'pk': a.pk
            } for a in Attachment.objects.filter(person_id=p.pk)
        ]

        previous_states = map(node_number_to_name, get_previous_nodes(p.state))
        next_states = map(node_number_to_name, get_next_nodes(p.state))
        state = ''
        state_name = WORKFLOW_STATES[p.state]
        if previous_states:
            state += '<a href="#down" id="downButton' + str(p.pk) + '">'\
                     '<img src="/static/img/boltdown.png">' \
                     '</a>' \
                     '<script>$(function(){ $("#downButton' + str(p.pk) + \
                     '").popover({content: "'
            popover_content = '<p>' + '</p><p>'.join(previous_states) + '</p>'
            state += popover_content
            state += '", placement: "left", trigger: "focus",' + \
                     'html: true});});</script>'
        state += state_name
        if next_states:
            state += '<a href="#up" id="upButton' + str(p.pk) + '">' \
                     '<img src="/static/img/bolt.png">' \
                     '</a>' \
                     '<script>$(function(){ $("#upButton' + str(p.pk) + \
                     '").popover({content: "'
            popover_content = '<p>' + '</p><p>'.join(next_states) + '</p>'
            state += popover_content
            state += '", placement: "right", trigger: "focus",' + \
                     'html: true});});</script>'
        resp.append({
            'id': p.pk,
            'candidateName': candidateName,
            'contact': contact,
            'state': state,
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
    person.state += 2
    person.save()
    return HttpResponse(200, content_type="plain/text")


def down(request, candidate_id):
    person = Person.objects.get(id=candidate_id)
    person.state += 1
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
    if Person.objects.filter(
            first_name=first_name,
            last_name=last_name
    ).exists():
        person = Person.objects.filter(
            first_name=first_name,
            last_name=last_name
        ).first()
        return HttpResponse(
            status=418,
            content_type="plain/text",
            content=person.state
        )
    else:
        Person.objects.create_person(
            first_name,
            last_name,
            args[2]
        )
        return HttpResponse(status=200, content=200, content_type="plain/text")


def stats(request):
    context = {
        'spices': [{
            'num': len(Person.objects.filter(state=k)),
            'name': v
        } for k, v in WORKFLOW_STATES.iteritems()]
    }
    return render(request, "stats.html", context)
