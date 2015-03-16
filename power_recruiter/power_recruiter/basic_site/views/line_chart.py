import datetime

from django.shortcuts import render
from power_recruiter.basic_site.workflow import WORKFLOW_STATES, get_states_dict
from power_recruiter.candidate.models import Person, OldState


def add_to_double_directory(first_directory, date, value, min_date, max_date):

    if date in first_directory:
        first_directory[date] += value
    else:
        first_directory[date] = value

    if date < min_date:
        min_date = date
    if date > max_date:
        max_date = date
    return min_date, max_date


def line_chart(request):
    db_states = get_states_dict()
    state_dict = {}
    for _, state in db_states.iteritems():
        state_dict[state.get_name()] = {}

    max_date = datetime.date(year=datetime.MINYEAR, month=1, day=1)
    min_date = datetime.date(year=datetime.MAXYEAR, month=1, day=1)

    for person in Person.objects.all():
        (min_date, max_date) = add_to_double_directory(
            state_dict[db_states[person.state].get_name()],
            person.current_state_started.date(),
            1,
            min_date,
            max_date
            )

    for old_state in OldState.objects.all():
        (min_date, max_date) = add_to_double_directory(
            state_dict[db_states[old_state.state].get_name()],
            old_state.start_date.date(),
            1,
            min_date,
            max_date
            )

        (min_date, max_date) = add_to_double_directory(
            state_dict[db_states[old_state.state].get_name()],
            old_state.change_date.date(),
            -1,
            min_date,
            max_date
            )

    result = {}

    for state in state_dict:
        current_state = []
        value = 0
        current_date = min_date
        while current_date <= max_date:
            if current_date in state_dict[state]:
                value += state_dict[state][current_date]
            current_state.append((str(current_date), value))
            current_date += datetime.timedelta(days=1)
        result[state] = current_state

    context = {
        'dicts': result
    }
    return render(request, "line_chart.html", context)
