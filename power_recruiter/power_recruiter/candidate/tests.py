from django.test import TestCase

from power_recruiter.candidate.models import Person


class TestPerson(TestCase):

    fixtures = ['graph.json', 'required.json']

    def test_get_conflicts(self):
        self.assertTrue(Person.get_conflicts() == [])

        first_name = "Cezary"
        last_name = "Kotko"
        photo_url = "http://kokso.wtf/cezary.jpeg"

        new_person1 = Person.objects.create_person(
            first_name=first_name,
            last_name=last_name,
            l_link="http://www.linkedin.com/costam1",
            photo_url=photo_url,
        )
        new_person1.save()
        new_person2 = Person.objects.create_person(
            first_name=first_name,
            last_name=last_name,
            l_link="http://www.linkedin.com/costam2",
            photo_url=photo_url,
        )
        new_person2.save()

        conflicts = Person.get_conflicts()

        self.assertEqual(set(conflicts), {new_person1, new_person2})

        new_person1.conflict_resolved = True
        new_person1.save()

        self.assertEqual(set(conflicts), {new_person1, new_person2})

        new_person2.conflict_resolved = True
        new_person2.save()

        self.assertTrue(Person.get_conflicts() == [])
