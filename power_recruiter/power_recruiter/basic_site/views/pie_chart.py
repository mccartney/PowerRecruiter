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

from django.shortcuts import render
from django.conf import settings

from power_recruiter.candidate.models import Person, State


def create_pie_chart_context():
    return {
        "static_js": settings.STATIC_JS_PATH,
        'spices': [{
            'num': len(Person.objects.filter(state=state)),
            'name': state.get_name()
        } for state in State.objects.all()]
    }


def pie_chart(request):
    return render(request, "pie_chart.html", create_pie_chart_context())
