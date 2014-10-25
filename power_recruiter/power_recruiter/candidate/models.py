from django.db import models


class Attachment(models.Model):
    name = models.CharField(max_length=100, default='')


class RecruitmentState(models.Model):
    name = models.CharField(max_length=100, default='')


class InternetLocation(models.Model):
    name = models.CharField(max_length=100, default='')


class Role(models.Model):
    name = models.CharField(max_length=100, default='')


class Communication(models.Model):
    name = models.CharField(max_length=100, default='')


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateField()

    state = models.ForeignKey(RecruitmentState)
    from_where = models.ForeignKey(InternetLocation)
    role = models.ForeignKey(Role)
    comm = models.ForeignKey(Communication)
    attachments = models.ManyToManyField(Attachment)
    caveats = models.CharField(max_length=1000)