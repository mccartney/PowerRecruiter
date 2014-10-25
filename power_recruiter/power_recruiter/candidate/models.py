from django.db import models


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


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateField()

    state = models.ForeignKey(RecruitmentState)
    source = models.ForeignKey(Source)
    role = models.ForeignKey(Role)
    comm = models.ForeignKey(Communication)
    caveats = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Attachment(models.Model):
    person = models.ForeignKey(Person, default=1)
    name = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name