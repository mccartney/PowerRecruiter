from power_recruiter.basic_site.models import State, Edge


def get_states_dict():
    states = State.objects.all()
    k = len(states)
    return dict(zip(range(k), states))


def get_next_nodes(node):
    edges = Edge.objects.filter(state_out=node)
    return [e.state_in.pk for e in edges]


def get_previous_nodes(node):
    edges = Edge.objects.filter(state_in=node)
    return [e.state_out.pk for e in edges]


def are_nodes_connected(first_node, second_node):
    a = len(Edge.objects.filter(state_out=first_node, state_in=second_node))
    b = len(Edge.objects.filter(state_out=second_node, state_in=first_node))
    return a+b > 0
