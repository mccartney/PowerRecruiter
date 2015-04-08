from django.utils import timezone
from django.db.models import Manager, Model, CharField, ForeignKey, \
    FileField, DateTimeField, TextField, URLField, EmailField, IntegerField, BooleanField
from django.template.loader import render_to_string

from power_recruiter.basic_site.workflow import get_next_nodes, get_previous_nodes
from power_recruiter.basic_site.models import Notification, State


class PersonManager(Manager):
    def create_person(self, first_name, last_name, link, photo_url):
        if "linkedin" in link:
            return self.create(
                first_name=first_name,
                last_name=last_name,
                linkedin=link,
                photo_url=photo_url
            )

        if "goldenline" in link:
            return self.create(
                first_name=first_name,
                last_name=last_name,
                goldenline=link,
                photo_url=photo_url
            )

        return self.create(
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url
        )


class Person(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    current_state_started = DateTimeField(default=timezone.now)
    state = ForeignKey(State, null=True)
    photo_url = CharField(max_length=200)
    linkedin = URLField(null=True, unique=True)
    goldenline = URLField(null=True, unique=True)
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
                return list(candidates)
        return []

    @classmethod
    def merge(cls, ids):
        # FIXME
        for person_id in ids[1:]:
            p = cls.objects.get(pk=person_id)
            p.delete()

    @classmethod
    def dont_merge(cls, ids):
        for person_id in ids:
            p = cls.objects.get(pk=person_id)
            p.conflict_resolved = True
            p.save()

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

        attachments = {
            'candidate_id': self.pk,
            'attachments': [{
                'display_name': str(a),
                'pk': a.pk
            } for a in Attachment.objects.filter(person_id=self.pk)]
        }

        previous_states = get_previous_nodes(self.state)

        next_states = get_next_nodes(self.state)

        state = {
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


class Attachment(Model):
    person = ForeignKey(Person)
    file = FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[23:]


class OldState(Model):
    person = ForeignKey(Person)
    start_date = DateTimeField(default=timezone.now)
    change_date = DateTimeField(default=timezone.now)
    state = ForeignKey(State, null=True)
