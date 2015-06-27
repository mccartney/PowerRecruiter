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

from django.conf.urls import patterns, url

from power_recruiter.basic_site.views.index import index
from power_recruiter.basic_site.views.pie_chart import pie_chart
from power_recruiter.basic_site.views.line_chart import line_chart
from power_recruiter.basic_site.views.jscoverage import jscoverage


urlpatterns = patterns(
    '',
    url(r'^$', index, name='home'),
    url(r'^pieChart$', pie_chart, name='pieChart'),
    url(r'^lineChart$', line_chart, name='lineChart'),
    url(r'^jscoverage-store/(?P<filename>.+)$', jscoverage, name='jscoverage')
)
