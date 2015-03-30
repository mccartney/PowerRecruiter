import datetime

from django.db.models import Model, IntegerField, TextField, CharField, \
    ForeignKey, BooleanField
from django.template.loader import render_to_string


class State(Model):
    name = CharField(max_length=100, default='')
    hired = BooleanField(default=False)
    rejected = BooleanField(default=False)

    def get_view(self):
        if self.hired:
            css_class = "greenText"
        elif self.rejected:
            css_class = "redText"
        else:
            css_class = "normalText"

        return render_to_string('state_name.html', {
            'css_class': css_class,
            'state_view': self.name
        })

    def get_name(self):
        return self.name

    def __unicode__(self):
        return self.get_view()

<<<<<<< HEAD
    def to_json(self):
        return self.get_view()

=======
>>>>>>> 2d792a4e7bd1936a998e223f4509d2bcf7b7ba5e
    @staticmethod
    def get_instance_name(name, hired=False, rejected=False):
        return ''.join([name, str(hired), str(rejected)])


class Edge(Model):
    state_out = ForeignKey(State, related_name='s_out')
    state_in = ForeignKey(State, related_name='s_in')

    def __unicode__(self):
        return str(self.state_out) + " -> " + str(self.state_in)

    def get_view(self):
        return self.__unicode__()
    get_view.allow_tags = True


class Notification(Model):
    days = IntegerField(null=False)
    state = ForeignKey(State, null=True)
    message = TextField(max_length=1000, blank=False)

    def get_message(self, person):
        state_started = person.current_state_started.replace(tzinfo=None)
        current_time = datetime.datetime.now().replace(tzinfo=None)
        delta = current_time - state_started
        if delta.days >= self.days and person.state == self.state:
            return str(self)
        return None

    def __unicode__(self):
        return self.message

    def get_state_view(self):
        return self.state.get_view()
    get_state_view.allow_tags = True
