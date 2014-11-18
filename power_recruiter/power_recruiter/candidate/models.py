import datetime

from django.db import models


class RecruitmentState(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name

class Source(models.Model):
    linkedin = models.URLField(null=True, unique=True)
    goldenline = models.URLField(null=True, unique=True)
    email = models.EmailField(null=True, unique=True)

    def __unicode__(self):
	toReturn = "";
	if linkedin is not None:
	    toReturn += linkedin;        
	if goldenline is not None:
	    toReturn += goldenline;        
	if email is not None:
	    toReturn += email;        
		
	return toReturn


class Role(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class Communication(models.Model):
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name


class PersonManager(models.Manager):
    def create_person(self, first_name, last_name, source):
        person = self.create(
            first_name=first_name,
            last_name=last_name,
            date_created=datetime.datetime.now(),
            state=RecruitmentState.objects.get(pk=1),
            comm=Communication.objects.get(pk=1),
            source=Source.objects.create_source(source)
        )
        return person


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateField()

    state = models.ForeignKey(RecruitmentState)
    source = models.ForeignKey(Source)
    role = models.ForeignKey(Role, blank=True, null=True)
    comm = models.ForeignKey(Communication)
    caveats = models.TextField(max_length=1000, blank=True)

    objects = PersonManager()

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Attachment(models.Model):
    person = models.ForeignKey(Person, default=1)
    file = models.FileField(upload_to='attachments/%Y/%m/%d')

    def __unicode__(self):
        return self.file.name[23:]
