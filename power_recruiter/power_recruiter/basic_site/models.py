from django.db import models


class Attachment(models.Model):
    pass


class RecruitmentState(models.Model):
    pass


class InternetLocation(models.Model):
    pass


class Role(models.Model):
    pass

class Communication(models.Model):
    pass


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateField
    state = models.ForeignKey(RecruitmentState)

    from_where = models.ForeignKey(InternetLocation)
    role = models.ForeignKey(Role)
    comm = models.ForeignKey(Communication)
    attachments = models.ManyToManyField(Attachment)
    caveats = models.CharField(max_length=1000)