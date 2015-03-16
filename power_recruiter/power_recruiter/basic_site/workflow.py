from django.template.loader import render_to_string

# from power_recruiter.basic_site.utils import multiton
from power_recruiter.basic_site.models import State, Edge


# @multiton
# class State(object):
#     def __init__(self, name, hired=False, rejected=False):
#         if hired and rejected:
#             raise ValueError("Cannot be hired and rejected at the same time.")
#         self.name = name
#         self.hired = hired
#         self.rejected = rejected
#
#     def get_view(self):
#         if self.hired:
#             css_class = "greenText"
#         elif self.rejected:
#             css_class = "redText"
#         else:
#             css_class = "normalText"
#
#         return render_to_string('state_name.html', {
#             'css_class': css_class,
#             'state_view': self.name
#         })
#
#     def get_name(self):
#         return self.name
#
#     __str__ = get_view
#
#     @staticmethod
#     def get_instance_name(name, hired=False, rejected=False):
#         return ''.join([name, str(hired), str(rejected)])

#
# WORKFLOW_STATES = {
#     0: State("New"),
#     1: State("Rejected", rejected=True),
#     2: State("First message"),
#     3: State("No response", rejected=True),
#     4: State("Negative response", rejected=True),
#     5: State("Positive response"),
#     6: State("First meeting"),
#     7: State("Resigned", rejected=True),
#     8: State("More than one meeting"),
#     9: State("Rejected after meeting", rejected=True),
#     10: State("Hired", hired=True)
# }

#
# WORKFLOW_GRAPH = {
#     0: [1, 2],
#     1: [],
#     2: [3, 4, 5],
#     3: [],
#     4: [],
#     5: [6],
#     6: [7, 8, 9],
#     7: [],
#     8: [7, 9, 10],
#     9: [],
#     10: []
# }


def get_states_dict():
    states = State.objects.all()
    k = len(states)
    return dict(zip(range(k), states))


def get_next_nodes(node):
    edges = Edge.objects.filter(state_out = node)
    return [e.state_in.pk for e in edges]


def get_previous_nodes(node):
    edges = Edge.objects.filter(state_in = node)
    return [e.state_out.pk for e in edges]


def are_nodes_connected(first_node, second_node):
    a = len(Edge.objects.filter(state_out=first_node, state_in=second_node))
    b = len(Edge.objects.filter(state_out=second_node, state_in=first_node))
    return a+b > 0
