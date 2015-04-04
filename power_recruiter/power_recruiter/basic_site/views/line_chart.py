from collections import defaultdict
import datetime

from django.shortcuts import render
from power_recruiter.candidate.models import Person, OldState, State


def get_data_bounds(state_dict):
    min_date = datetime.date(year=datetime.MAXYEAR, month=1, day=1)
    max_date = datetime.date(year=datetime.MINYEAR, month=1, day=1)

    for date_dict in state_dict.values():
        for date, value in date_dict.iteritems():
            if date < min_date:
                min_date = date
            if date > max_date:
                max_date = date

    return min_date, max_date


def add_to_dictionary(state_dict, date, value):
    state_dict[date] += value


def line_chart(request):

    # Double dictionary: state -> {date -> numberOfCandidates}
    state_dict = {}
    for state in State.objects.all():
        state_dict[state.get_name()] = defaultdict(int)

    # Add all current states
    for person in Person.objects.all():
        add_to_dictionary(
            state_dict[person.state.get_name()],
            person.current_state_started.date(),
            1
        )

    # Add all old states
    for old_state in OldState.objects.all():
        add_to_dictionary(
            state_dict[old_state.state.get_name()],
            old_state.start_date.date(),
            1
        )

        add_to_dictionary(
            state_dict[old_state.state.get_name()],
            old_state.change_date.date(),
            -1
        )

    (min_date, max_date) = get_data_bounds(state_dict)

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
