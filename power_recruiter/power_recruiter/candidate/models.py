from django.utils import timezone
from django.db.models import Manager, Model, CharField, ForeignKey, \
    FileField, DateField, DateTimeField, TextField, URLField, EmailField, IntegerField
from django.template.loader import render_to_string

from power_recruiter.basic_site.workflow import WORKFLOW_STATES, \
    get_next_nodes, get_previous_nodes


class ContactManager(Manager):
    def create_contact(self, link):
        if "linkedin" in link:
            communication = self.create(linkedin=link)
            return communication

        if "goldenline" in link:
            communication = self.create(goldenline=link)
            return communication

        contact = self.create()
        return contact


class Contact(Model):
    linkedin = URLField(null=True, unique=True)
    goldenline = URLField(null=True, unique=True)
    email = EmailField(null=True, unique=True)

    objects = ContactManager()

    def __unicode__(self):
        return u"".join([
            self.linkedin or u"",
            self.goldenline or u"",
            self.email or u""
        ])


class Role(Model):
    name = CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class PersonManager(Manager):
    def create_person(self, first_name, last_name, link, photo_url):
        person = self.create(
            first_name=first_name,
            last_name=last_name,
            contact=Contact.objects.create_contact(link),
            photo_url=photo_url
        )
        return person


class Person(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    current_state_started = DateField(default=timezone.now)
    state = IntegerField(default=0)
    photo_url = CharField(max_length=200)
    contact = ForeignKey(Contact)
    role = ForeignKey(Role, blank=True, null=True)
    caveats = TextField(max_length=1000, blank=True)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def to_json(self):
        id = {
            'id': self.pk,
        }

        photo = {
            'photo': self.photo_url,
        }

        candidate_name = {
            'candidateId': self.pk,
            'candidateName': str(self),
        }

        contact = {
            'candidateId': self.pk,
            'candidateName': str(self),
            'linkedin': self.contact.linkedin,
            'goldenline': self.contact.goldenline,
            'email': self.contact.email,
        }

        attachments = {
            'candidateId': self.pk,
            'attachments': [{
                'display_name': str(a),
                'pk': a.pk
            } for a in Attachment.objects.filter(person_id=self.pk)]
        }

        previous_states = {k: WORKFLOW_STATES[k]
                           for k in get_previous_nodes(self.state)}
        next_states = {k: WORKFLOW_STATES[k]
                       for k in get_next_nodes(self.state)}

        state = {
            'state_name': WORKFLOW_STATES[self.state].name,
            'current_state_started': str(self.current_state_started),
            'state_view': render_to_string('state.html', {
                'person_id': self.pk,
                'previous_states': previous_states,
                'next_states': next_states,
                'state_view': WORKFLOW_STATES[self.state]
                }),
            'state_history':  [{
                'startDate': str(oldState.changeDate.date()),
                'changeDate': str(oldState.changeDate.date()),
                'state': str(WORKFLOW_STATES[oldState.state])
            } for oldState in OldState.objects.filter(person_id=self.pk).order_by('-changeDate')]
        }

        caveats = {
            'candidateId': self.pk,
            'candidateName': str(self),
            'caveats': self.caveats
        }

        return {
            'id': id,
            'photo' : photo,
            'candidateName': candidate_name,
            'contact': contact,
            'state': state,
            'attachments': attachments,
            'caveats': caveats,
        }


class Attachment(Model):
    person = ForeignKey(Person)
    file = FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[23:]


class OldState(Model):
    person = ForeignKey(Person)
    startDate = DateTimeField(default=timezone.now)
    changeDate = DateTimeField(default=timezone.now)
    state = IntegerField(default=0)
