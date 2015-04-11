from django.test import TestCase, Client

from power_recruiter.candidate.models import Person,Attachment
from power_recruiter.settings import BASE_DIR


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


class TestCandidateView(TestCase):

    fixtures = ['graph.json', 'required.json']

    def verify_file_content(self, file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEquals(file_content, "12345\nala ma kota\n")
        file.closed

    def test_attachment(self):
        c = Client(enforce_csrf_checks=False)
        self.assertEqual(len(Attachment.objects.all()), 0)

        # Add file
        with open(BASE_DIR + '/power_recruiter/tests/upload_files/readme.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/', {'person': '2', 'file': fp}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 1)
        self.assertEqual(Attachment.objects.all()[0].pk, 1)

        # There is an issue with Client downloading MEDIA_ROOT files
        # then we only get URL, then open this file with PYTHON
        response_get = c.get('/candidate/attachment/get/1', follow=True)
        self.assertEquals(response_get.status_code, 200)

        file_path = response_get.redirect_chain[0][0][len("http://testserver/"):]
        self.verify_file_content(file_path)

        # Add second file to same person
        self.assertEqual(len(Attachment.objects.all()), 1)
        with open(BASE_DIR + '/power_recruiter/tests/upload_files/list.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/', {'person': '3', 'file': fp}, follow=True)

        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 2)
        self.assertEqual(Attachment.objects.all()[0].pk, 1)
        self.assertEqual(Attachment.objects.all()[1].pk, 2)

        # Remove first file
        response_remove = c.post('/candidate/attachment/remove/', {'id': 1}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 1)
        self.assertEqual(Attachment.objects.all()[0].pk, 2)
        self.assertEqual("list", str(Attachment.objects.all()[0])[:len("list")])

        # It's safe remove after all
        self.verify_file_content(file_path)

    def test_change_name(self):
        c = Client(enforce_csrf_checks=False)
        kamila = Person.objects.get(pk=2)
        self.assertEqual(kamila.first_name, "Kamila")
        self.assertEqual(kamila.last_name, "Kruk")
        response_post = c.post('/candidate/change_name/', {'id': 2, 'name': 'Kamilsha von Kruk - Kowalska'}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        kamila = Person.objects.get(pk=2)
        self.assertEqual(kamila.first_name, "Kamilsha")
        self.assertEqual(kamila.last_name, "von Kruk - Kowalska")


