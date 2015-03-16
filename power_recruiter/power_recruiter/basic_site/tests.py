from django.test import TestCase

from power_recruiter.basic_site.workflow import get_next_nodes, \
    get_previous_nodes, get_states_list, WORKFLOW_GRAPH, State


class TestWorkflow(TestCase):
    # def test_get_next_nodes(self):
        # self.assertEqual(WORKFLOW_GRAPH[6], get_next_nodes(6))
        # self.assertEqual(WORKFLOW_GRAPH[10], get_next_nodes(10))

    # def test_get_previous_nodes(self):
    #     self.assertEqual([6, 8], sorted(get_previous_nodes(7)))
    #     self.assertEqual([], get_previous_nodes(0))
    #
    # def test_get_states_list(self):
    #     self.assertIn(State("First meeting"), get_states_list())
    #     self.assertIn(State("Hired", hired=True), get_states_list())
    #     self.assertIn(State("Resigned", rejected=True), get_states_list())
    #     self.assertNotIn(State("Drunk"), get_states_list())

    # def test_state(self):
    #     with self.assertRaises(ValueError):
    #         State("awdawda", hired=True, rejected=True)
    pass
