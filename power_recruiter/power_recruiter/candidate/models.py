from django.utils import timezone
from django.db.models import Manager, Model, CharField, ForeignKey, \
    FileField, DateTimeField, TextField, URLField, EmailField, BooleanField
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from power_recruiter.basic_site.workflow import get_next_nodes, get_previous_nodes
from power_recruiter.basic_site.models import Notification, State
import datetime


class PersonManager(Manager):
    def create_person(self, first_name, last_name, photo_url="", l_link="", g_link="", m_link=""):
        l_link = None if not l_link else l_link
        g_link = None if not g_link else g_link
        m_link = None if not m_link else m_link
        return self.create(
            state=State.objects.get(pk=1),
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url,
            linkedin=l_link,
            goldenline=g_link,
            email=m_link
        )


class Person(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    current_state_started = DateTimeField(default=timezone.now)
    state = ForeignKey(State, null=True)
    photo_url = CharField(max_length=200)
    linkedin = URLField(null=True, unique=False)
    goldenline = URLField(null=True, unique=False)
    email = EmailField(null=True, unique=False)
    caveats = TextField(max_length=1000, blank=True)
    conflict_resolved = BooleanField(default=False)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    @classmethod
    def get_conflicts(cls):
        all_candidates = cls.objects.filter(conflict_resolved=False)
        for c in all_candidates:
            candidates = cls.objects.filter(
                first_name=c.first_name,
                last_name=c.last_name
            )
            if len(candidates) > 1:
                return candidates
        return []

    @classmethod
    def merge(cls, ids, photo, state):
        rids = []
        for i in ids:
            rids.append(int(i))
        photo = int(photo)
        state = int(state)
        right_person = Person.objects.get(id=rids[0])
        wrong_person = Person.objects.get(id=rids[1])
        state_person = Person.objects.get(id=rids[state])
        if right_person.state != state_person.state:
            right_person.update_state(state_person.state.id)
        right_person.photo_url = Person.objects.get(id=rids[photo]).photo_url
        old_atts = Attachment.objects.filter(person=wrong_person)
        for o in old_atts:
            o.person = right_person
        right_person.save()
        wrong_person.delete()

    @classmethod
    def dont_merge(cls, ids):
        for person_id in ids:
            p = cls.objects.get(pk=person_id)
            p.conflict_resolved = True
            p.save()

    def update_state(self, new_state_id):
        old_state = OldState(
            person=self,
            start_date=self.current_state_started,
            change_date=datetime.datetime.now(),
            state=self.state
        )
        old_state.save()
        self.state = get_object_or_404(State, id=new_state_id)
        self.current_state_started = datetime.datetime.now()
        self.save()

    def to_json(self):
        id = {
            'id': self.pk,
        }

        photo = {
            'photo': self.photo_url,
            'notifications': [{
                'message': str(msg)
            } for msg in self.get_person_notifications()]
        }

        candidate_name = {
            'candidate_id': self.pk,
            'candidate_name': str(self),
        }

        contact = {
            'candidate_id': self.pk,
            'candidate_name': str(self),
            'linkedin': self.linkedin,
            'goldenline': self.goldenline,
            'email': self.email,
        }

        previous_states = get_previous_nodes(self.state)

        next_states = get_next_nodes(self.state)

        state = {
            'raw_state_name': str(self.state.get_name()),
            'state_name': str(self.state),
            'current_state_started': str(self.current_state_started.date()),
            'state_view': render_to_string('state.html', {
                'person_id': self.pk,
                'previous_states': previous_states,
                'next_states': next_states,
                'state_view': str(self.state)
            }),
            'state_history':  [
                {
                    'start_date': str(oldState.start_date.date()),
                    'change_date': str(oldState.change_date.date()),
                    'state': str(oldState.state)
                } for oldState in OldState.objects.filter(person_id=self.pk).order_by('-change_date')
            ]
        }

        attachments = {
            'candidate_id': self.pk,
            'attachments': [{
                'display_name': str(a),
                'pk': a.pk
            } for a in Attachment.objects.filter(person_id=self.pk)]
        }

        caveats = {
            'candidate_id': self.pk,
            'candidate_name': str(self),
            'caveats': self.caveats
        }

        return {
            'id': id,
            'photo': photo,
            'candidate_name': candidate_name,
            'contact': contact,
            'state': state,
            'attachments': attachments,
            'caveats': caveats,
        }

    def get_person_notifications(self):
        notifications = []
        for notification in Notification.objects.all():
            if notification.get_message(self):
                notifications.append(notification.get_message(self))
        return notifications

    def get_state_view(self):
        return self.state.get_view()
    get_state_view.allow_tags = True

class Attachment(Model):
    person = ForeignKey(Person)
    file = FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[len("attachments/YYYY/MM/DD/"):]


class OldState(Model):
    person = ForeignKey(Person)
    start_date = DateTimeField(default=timezone.now)
    change_date = DateTimeField(default=timezone.now)
    state = ForeignKey(State, null=True)