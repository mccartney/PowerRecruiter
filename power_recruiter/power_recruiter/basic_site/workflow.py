# https://www.python.org/doc/essays/graphs/

WORKFLOW_STATES = {
    0: 'NULL',
    1: 'Rejected',
    2: 'First message',
    3: 'No response',
    4: 'Negative response',
    5: 'Positive response',
    6: '1s',
    7: 'Resigned',
    8: '>1',
    9: 'Rejected after meeting',
    10: 'Hired'
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
