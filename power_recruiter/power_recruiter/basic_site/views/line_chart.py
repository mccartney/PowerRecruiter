"""
Power Recruiter - a browser-based FSM-centered database application profiled for IT recruiters
Copyright (C) 2015 Krzysztof Fudali, Andrzej Jackowski, Cezary Kosko, Filip Ochnik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import defaultdict
import datetime

from django.shortcuts import render
from django.conf import settings
from power_recruiter.candidate.models import Person, OldState, State


def get_data_bounds(state_dict):
    min_date = datetime.date(year=datetime.MAXYEAR, month=1, day=1)
    max_date = datetime.date(year=datetime.MINYEAR, month=1, day=1)

    for date_dict in state_dict.values():
        for date, _ in date_dict.iteritems():
            if date < min_date:
                min_date = date
            if date > max_date:
                max_date = date

    return min_date, max_date


def add_to_dictionary(state_dict, date, value):
    state_dict[date] += value


def generate_result(state_dict, min_date, max_date):
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

    return result


def generate_context_dicts():
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

    min_date, max_date = get_data_bounds(state_dict)
    return generate_result(state_dict, min_date, max_date)


def line_chart(request):
    context = {
        'dicts': generate_context_dicts(),
        "static_js": settings.STATIC_JS_PATH
    }
    return render(request, "line_chart.html", context)
