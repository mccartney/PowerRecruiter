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

from power_recruiter.candidate.models import Attachment, Person, State
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


def upload_attachment(request):
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

def get_attachment(request, attachment_id):
    attachment = Attachment.objects.get(pk=attachment_id)
    return redirect(attachment.file.url)

@require_POST
def remove_attachment(request):
    try:
        attachment_id = int(request.POST['id'])
    except KeyError:
        raise Http404
    to_remove = get_object_or_404(Attachment, pk=attachment_id)

    # IMO the file should stay on server
    #to_remove.file.delete()

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
        if not int(request.GET.get("state%d" % state.pk, 1)):
            persons = persons.exclude(state=state)
    response = [p.to_json() for p in persons]
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_POST
def caveats_upload(request):
    try:
        person_id = int(request.POST['id'])
        caveats = request.POST['caveats']
        #Dividing by 1000 is required, cuz js and python have different timestamps
        timestamp = datetime.datetime.fromtimestamp(int(request.POST['timestamp'])/1000.0)
    except KeyError:
        raise Http404
    person = get_object_or_404(Person, id=person_id)

    if timestamp > person.caveats_timestamp.replace(tzinfo=None):
        person.caveats = caveats
        person.save()

    return HttpResponse(200, content_type="plain/text")


@require_POST
def change_state(request):
    try:
        person_id = int(request.POST['person_id'])
        new_state_id = int(request.POST['new_state_id'])
    except KeyError:
        raise Http404
    person = get_object_or_404(Person, id=person_id)
    if are_nodes_connected(new_state_id, person.state.pk):
        person.update_state(new_state_id)
        return HttpResponse(200, content_type="plain/text")
    raise Http404

@csrf_exempt
def add_candidate(request):
    args = []
    for i in xrange(3):
        args.append(request.POST['args[%d]' % i])
    names = args[0].split(' ')
    first_name = names[0]
    last_name = names[-1]
    l_link=""
    g_link=""
    link = args[2]
    if "linkedin" in link:
        l_link = link
    if "goldenline" in link:
        g_link = link
    Person.objects.create_person(
        first_name=first_name,
        last_name=last_name,
        photo_url=args[1],
        l_link=l_link,
        g_link=g_link
    )
    return HttpResponse(status=200, content=200, content_type="plain/text")

def add_candidate_from_app(request):
    Person.objects.create_person(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        g_link=request.POST['goldenline_link'],
        l_link=request.POST['linkedin_link'],
        m_link=request.POST['email_link']
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
    photo = request.POST.get('person_img')
    state = request.POST.get('person_state')
    merge = json.loads(request.POST.get('merge'))
    if merge:
        Person.merge(person_ids, photo, state)
    else:
        Person.dont_merge(person_ids)
    return HttpResponse(status=200, content=200, content_type="plain/text")
