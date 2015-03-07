from django.db.models import Manager, Model, IntegerField, TextField
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
