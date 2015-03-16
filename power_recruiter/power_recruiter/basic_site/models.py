from django.db.models import Model, IntegerField, TextField, CharField, ForeignKey
import datetime


class Notification(Model):
    days = IntegerField(null=False)
    state = IntegerField(null=False)
    message = TextField(max_length=1000, blank=False)

    def get_message(self, person):
        state_started = person.current_state_started.replace(tzinfo=None)
        current_time = datetime.datetime.now().replace(tzinfo=None)
        delta = current_time - state_started
        if delta.days > self.days and person.state == self.state:
            return str(self)
        return None

    def __unicode__(self):
        return self.message

class State(Model):
    name = CharField(max_length=100, default='')

    def __unicode__(self):
        return self.name

class Edge(Model):
    state_out = ForeignKey(State, related_name='s_out')
    state_in = ForeignKey(State, related_name='s_in')

    def __unicode__(self):
        return str(self.state_out) + " -> " + str(self.state_in)