from django.db import models
import datetime


class RecruitmentState(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class Communication(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class PersonManager(models.Manager):
    def create_person(self, first_name, last_name):
        person = self.create(first_name=first_name, last_name=last_name, date_created=datetime.datetime.now(), state=RecruitmentState.objects.get(pk=1), comm=Communication.objects.get(pk=1), source=Source.objects.get(pk=1), role=Role.objects.get(pk=1))

        return person


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateField()

    state = models.ForeignKey(RecruitmentState)
    source = models.ForeignKey(Source)
    role = models.ForeignKey(Role, blank=True, null=True)
    comm = models.ForeignKey(Communication)
    caveats = models.CharField(max_length=1000, blank=True)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Attachment(models.Model):
    person = models.ForeignKey(Person, default=1)
    name = models.CharField(max_length=100, default='')
    file = models.FileField(upload_to='attachments/')

    def __unicode__(self):
        return self.name