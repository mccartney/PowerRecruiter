import datetime

from django.shortcuts import render
from power_recruiter.candidate.models import Person, OldState, State


def add_to_dictionary_return_minmax(state_dict, date, value, min_date, max_date):

    if date in state_dict:
        state_dict[date] += value
    else:
        state_dict[date] = value

    if date < min_date:
        min_date = date
    if date > max_date:
        max_date = date

    return min_date, max_date


def line_chart(request):
    # Begining and end of statistics (x-axis)
    min_date = datetime.date(year=datetime.MAXYEAR, month=1, day=1)
    max_date = datetime.date(year=datetime.MINYEAR, month=1, day=1)

    # Double dictionary: state -> {date -> numberOfCandidates}
    state_dict = {}
    for state in State.objects.all():
        state_dict[state.get_name()] = {}

    # Add all current states
    for person in Person.objects.all():
        (min_date, max_date) = add_to_dictionary_return_minmax(
            state_dict[person.state.get_name()],
            person.current_state_started.date(),
            1,
            min_date,
            max_date
        )

    # Add all old states
    for old_state in OldState.objects.all():
        (min_date, max_date) = add_to_dictionary_return_minmax(
            state_dict[old_state.state.get_name()],
            old_state.start_date.date(),
            1,
            min_date,
            max_date
            )

        (min_date, max_date) = add_to_dictionary_return_minmax(
            state_dict[old_state.state.get_name()],
            old_state.change_date.date(),
            -1,
            min_date,
            max_date
            )

    # Generate results
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
