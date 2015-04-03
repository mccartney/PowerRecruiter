from django.test import TestCase
from power_recruiter.basic_site.models import State

from power_recruiter.basic_site.workflow import get_next_nodes, get_previous_nodes, are_nodes_connected

def get_state_by_name(name):
    return State.objects.get(name=name)

class TestWorkflow(TestCase):
    fixtures = ['graph.json']
    def test_state_num(self):
        self.assertEqual(len(State.objects.all()), 11)

    def test_get_next_nodes(self):
        self.assertEqual([], get_next_nodes(get_state_by_name("Hired")))
        self.assertEqual([
            get_state_by_name("No response"),
            get_state_by_name("Negative response"),
            get_state_by_name("Positive response")
        ], get_next_nodes(get_state_by_name("First message")))

    def test_get_previous_nodes(self):
         self.assertEqual([], get_previous_nodes(get_state_by_name("New")))
         self.assertEqual([
            get_state_by_name("First meeting"),
            get_state_by_name("More than one meeting")
        ], get_previous_nodes(get_state_by_name("Resigned")))

    def test_are_nodes_connected(self):
        self.assertTrue(are_nodes_connected(get_state_by_name("New"), get_state_by_name("First message")))
        self.assertTrue(are_nodes_connected(get_state_by_name("Negative response"), get_state_by_name("First message")))
        self.assertFalse(are_nodes_connected(get_state_by_name("Negative response"), get_state_by_name("No response")))
        self.assertFalse(are_nodes_connected(get_state_by_name("Hired"), get_state_by_name("New")))
