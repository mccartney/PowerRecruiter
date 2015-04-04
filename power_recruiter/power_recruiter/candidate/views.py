import json
import logging
import sys
import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django import forms
from django.core.urlresolvers import reverse
from django.template import RequestContext

from power_recruiter.candidate.models import Attachment, Person, OldState, State
from power_recruiter.basic_site.workflow import are_nodes_connected


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


@require_POST
def remove_attachment(request):
    try:
        attachment_id = int(request.POST['id'])
    except KeyError:
        raise Http404
    to_remove = Attachment.objects.get(pk=attachment_id)
    to_remove.file.delete()
    to_remove.delete()
    return HttpResponse(200, content_type="plain/text")


@require_POST
def change_name(request):
    try:
        person_id = int(request.POST['id'])
        new_name = request.POST['name']
    except KeyError:
        raise Http404
    person = get_object_or_404(Person, id=person_id)
    new_name = new_name.strip()
    names = new_name.split()
    person.first_name = names[0]
    person.last_name = " ".join(names[1:])
    person.save()
    return HttpResponse(200, content_type="plain/text")


@require_POST
def remove_person(request):
    try:
        person_id = int(request.POST['id'])
    except KeyError:
        raise Http404
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return HttpResponse(200, content_type="plain/text")


def candidate_json(request):
    persons = Person.objects.all()
    for state in State.objects.all():
        if request.GET.get(state, False):
            persons = persons.exclude(state=state)
    response = [p.to_json() for p in persons]
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_POST
@csrf_exempt  # Do we need it? I think we have csrf ajax done at js level
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


@require_POST
def change_state(request):
    try:
        person_id = int(request.POST['person_id'])
        new_state_id = int(request.POST['new_state_id'])
    except KeyError:
        raise Http404
    person = get_object_or_404(Person, id=person_id)
    if are_nodes_connected(new_state_id, person.state):
        old_state = OldState(
            person=person,
            start_date=person.current_state_started,
            change_date=datetime.datetime.now(),
            state=person.state
        )
        old_state.save()
        person.state = get_object_or_404(State, id=new_state_id)
        person.current_state_started = datetime.datetime.now()
        person.save()
        return HttpResponse(200, content_type="plain/text")
    raise Http404


@csrf_exempt  # Do we need it?
def add_candidate(request):
    db_states = get_states_dict()
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
            content=db_states[person.state].name
        )
    else:
        Person.objects.create_person(
            first_name,
            last_name,
            args[2],
            args[1]
        )
        return HttpResponse(status=200, content=200, content_type="plain/text")


def get_conflicts(request):
    conflicting_candidates = Person.get_conflicts()
    response = [c.to_json() for c in conflicting_candidates],
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_POST
def resolve_conflicts(request):
    person_ids_json = request.POST.get('person_ids')
    person_ids = json.loads(person_ids_json)
    merge = json.loads(request.POST.get('merge'))
    if merge:
        Person.merge(person_ids)
    else:
        Person.dont_merge(person_ids)
    return HttpResponse(status=200, content=200, content_type="plain/text")
