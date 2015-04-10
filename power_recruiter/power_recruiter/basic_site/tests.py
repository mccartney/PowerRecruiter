from django.test import TestCase

from power_recruiter.basic_site.models import State
from power_recruiter.basic_site.workflow import get_next_nodes, get_previous_nodes, are_nodes_connected
from power_recruiter.basic_site.views.pie_chart import create_pie_chart_context
from power_recruiter.basic_site.views.line_chart import generate_context_dicts

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

class TestCharts(TestCase):

    fixtures = ['graph.json', 'required.json']

    def test_pie_chart(self):
        correct_chart = {'spices': [
            {'name': u'New', 'num': 0},
            {'name': u'Rejected', 'num': 0},
            {'name': u'First message', 'num': 1},
            {'name': u'No response', 'num': 0},
            {'name': u'Negative response', 'num': 1},
            {'name': u'Positive response', 'num': 0},
            {'name': u'First meeting', 'num': 1},
            {'name': u'Resigned', 'num': 1},
            {'name': u'More than one meeting', 'num': 0},
            {'name': u'Rejected after meeting', 'num': 0},
            {'name': u'Hired', 'num': 2}
        ]}
        self.assertTrue(correct_chart, create_pie_chart_context())

    def get_value_for_state_and_date(self, state, date):
        for pair in generate_context_dicts()[state]:
            if pair[0] == date:
                return pair[1]

    def test_line_chart(self):
        self.assertEqual(self.get_value_for_state_and_date("New", "2014-11-28"), 1)
        self.assertEqual(self.get_value_for_state_and_date("New", "2014-12-08"), 3)
        self.assertEqual(self.get_value_for_state_and_date("New", "2014-12-19"), 0)
        self.assertEqual(self.get_value_for_state_and_date("Hired", "2015-03-07"), 2)