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

import urllib2

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# This workaround is used to save javascript coverage report
# while using both Django and jscoverage server
@csrf_exempt
def jscoverage(request, filename):
    urllib2.urlopen('http://127.0.0.1:8081/jscoverage-store/' + filename,
                    request.read())
    return HttpResponse(status=200)
