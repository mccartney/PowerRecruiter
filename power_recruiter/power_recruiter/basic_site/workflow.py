from django.template.loader import render_to_string

class State:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_name(self):
        return self.name

    def get_view(self):
        if self.type != 0:
            if self.type == 1:
                css_class = "greenText"
            else:
                css_class = "redText"

            return render_to_string('state_name.html', {
               'css_class': css_class,
               'state_view': self.name
            })

        return self.name

    def __str__(self):
        return self.get_view()

WORKFLOW_STATES = {
    0: State('New', 0),
    1: State('Rejected', -1),
    2: State('First message', 0),
    3: State('No response', -1),
    4: State('Negative response', -1),
    5: State('Positive response', 0),
    6: State('First meeting', 0),
    7: State('Resigned', -1),
    8: State('More than one meeting', 0),
    9: State('Rejected after meeting', -1),
    10: State('Hired', 1)
}

WORKFLOW_GRAPH = {
    0: [1, 2],
    1: [],
    2: [3, 4, 5],
    3: [],
    4: [],
    5: [6],
    6: [7, 8, 9],
    7: [],
    8: [7, 9, 10],
    9: [],
    10: []
}


def get_next_nodes(node):
    return WORKFLOW_GRAPH[node]


def get_previous_nodes(node):
    previous_nodes = [k for k, v in WORKFLOW_GRAPH.iteritems() if node in v]
    return previous_nodes


def get_states_list():
    return WORKFLOW_STATES.values()


def are_nodes_connected(first_node, second_node):
    return (
        first_node in WORKFLOW_GRAPH[second_node] or
        second_node in WORKFLOW_GRAPH[first_node]
    )
