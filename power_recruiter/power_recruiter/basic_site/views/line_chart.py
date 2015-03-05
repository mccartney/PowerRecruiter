import datetime

from django.shortcuts import render
from power_recruiter.basic_site.workflow import WORKFLOW_STATES
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
    return (min_date, max_date)


def line_chart(request):
    state_dict = {}
    for idx, state in WORKFLOW_STATES.iteritems():
        state_dict[state.get_name()] = {}

    max_date = datetime.date(year=datetime.MINYEAR, month=1, day=1)
    min_date = datetime.date(year=datetime.MAXYEAR, month=1, day=1)


    for person in Person.objects.all():
        (min_date, max_date) = add_to_double_directory(
            state_dict[WORKFLOW_STATES[person.state].get_name()],
            person.current_state_started.date(),
            1,
            min_date,
            max_date
            )

    for oldState in OldState.objects.all():
        (min_date, max_date) = add_to_double_directory(
            state_dict[WORKFLOW_STATES[oldState.state].get_name()],
            oldState.startDate.date(),
            1,
            min_date,
            max_date
            )

        (min_date, max_date) = add_to_double_directory(
            state_dict[WORKFLOW_STATES[oldState.state].get_name()],
            oldState.changeDate.date(),
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

