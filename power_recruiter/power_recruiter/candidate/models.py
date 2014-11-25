from django.utils import timezone
from django.db.models import Manager, Model, CharField, ForeignKey, \
    FileField, DateField, TextField, URLField, EmailField, IntegerField

from power_recruiter.basic_site.workflow import WORKFLOW_STATES


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
    def create_person(self, first_name, last_name, link):
        person = self.create(
            first_name = first_name,
            last_name = last_name,
            contact = Contact.objects.create_contact(link)
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
    contact = ForeignKey(Contact)
    role = ForeignKey(Role, blank=True, null=True)
    caveats = TextField(max_length=1000, blank=True)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Attachment(Model):
    person = ForeignKey(Person, default=1)
    file = FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[23:]
