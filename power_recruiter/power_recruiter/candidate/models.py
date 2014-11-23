from django.utils import timezone
from django.db.models import Manager, Model, CharField, ForeignKey, \
    FileField, DateField, TextField, URLField, EmailField, IntegerField

from power_recruiter.basic_site.workflow import WORKFLOW_STATES


class SourceManager(Manager):
    def create_source(self, name):
        if "linkedin" in name:
            source = self.create(linkedin=name)
            return source

        if "goldenline" in name:
            source = self.create(goldenline=name)
            return source

        if "@" in name:
            source = self.create(email=name)
            return source

        source = self.create()
        return source


class Source(Model):
    linkedin = URLField(null=True, unique=True)
    goldenline = URLField(null=True, unique=True)
    email = EmailField(null=True, unique=True)

    objects = SourceManager()

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


class Communication(Model):
    name = CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class PersonManager(Manager):
    def create_person(self, first_name, last_name, source):
        person = self.create(
            first_name=first_name,
            last_name=last_name,
            comm=Communication.objects.get(pk=1),
            source=Source.objects.create_source(source)
        )
        return person


class Person(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    date_created = DateField(default=timezone.now)
    state = IntegerField(
        choices=((k, v) for k, v in WORKFLOW_STATES.iteritems()),
        default=0
    )
    source = ForeignKey(Source)
    role = ForeignKey(Role, blank=True, null=True)
    comm = ForeignKey(Communication)
    caveats = TextField(max_length=1000, blank=True)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Attachment(Model):
    person = ForeignKey(Person, default=1)
    file = FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[23:]
