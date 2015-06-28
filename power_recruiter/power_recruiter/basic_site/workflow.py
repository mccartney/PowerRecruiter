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

from power_recruiter.basic_site.models import Edge


def get_next_nodes(node):
    return [state.state_in for state in Edge.objects.filter(state_out=node)]


def get_previous_nodes(node):
    return [state.state_out for state in Edge.objects.filter(state_in=node)]


def are_nodes_connected(first_node, second_node):
    return Edge.objects.filter(state_out=first_node, state_in=second_node) or \
        Edge.objects.filter(state_out=second_node, state_in=first_node)
