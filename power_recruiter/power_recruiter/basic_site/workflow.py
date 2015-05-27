from power_recruiter.basic_site.models import Edge


def get_next_nodes(node):
    return [state.state_in for state in Edge.objects.filter(state_out=node)]


def get_previous_nodes(node):
    return [state.state_out for state in Edge.objects.filter(state_in=node)]


def are_nodes_connected(first_node, second_node):
    return Edge.objects.filter(state_out=first_node, state_in=second_node) or \
        Edge.objects.filter(state_out=second_node, state_in=first_node)
