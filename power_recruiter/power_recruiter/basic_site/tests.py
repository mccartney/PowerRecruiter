from django.test import TestCase

from power_recruiter.basic_site.workflow import get_next_nodes, \
    get_previous_nodes, get_states_list, WORKFLOW_GRAPH


class TestWorkflow(TestCase):
    def test_get_next_nodes(self):
        self.assertEqual(WORKFLOW_GRAPH[6], get_next_nodes(6))
        self.assertEqual(WORKFLOW_GRAPH[10], get_next_nodes(10))

    def test_get_previous_nodes(self):
        self.assertEqual([6, 8], sorted(get_previous_nodes(7)))
        self.assertEqual([], get_previous_nodes(0))

    def test_get_states_list(self):
        self.assertIn('1s', get_states_list())
        self.assertIn('Hired', get_states_list())
