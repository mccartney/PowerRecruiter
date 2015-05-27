import json
import time
import datetime

from django.test import TestCase, Client
from django.test.utils import override_settings

from power_recruiter.candidate.models import Person, Attachment, OldState, \
    ResolvedConflict
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
            linkedin="http://www.linkedin.com/costam1",
            photo_url=photo_url,
        )
        new_person1.save()
        new_person2 = Person.objects.create_person(
            first_name=first_name,
            last_name=last_name,
            linkedin="http://www.linkedin.com/costam2",
            photo_url=photo_url,
        )
        new_person2.save()

        conflicts = Person.get_conflicts()
        self.assertEqual(set(conflicts), {new_person1, new_person2})

        resolved_conflicts = resolved_conflicts = ResolvedConflict(
            person_one=new_person1,
            person_two=new_person2
        )
        resolved_conflicts.save()

        self.assertTrue(Person.get_conflicts() == [])


class TestCandidateView(TestCase):
    fixtures = ['graph.json', 'required.json']

    def verify_file_content(self, file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            self.assertEquals(file_content, "12345\nala ma kota\n")
        self.assertTrue(file.closed)

    @override_settings(DEBUG=True)
    def test_attachment(self):
        c = Client(enforce_csrf_checks=False)
        self.assertEqual(len(Attachment.objects.all()), 0)

        # Add file
        with open(BASE_DIR +
                  '/power_recruiter/tests/upload_files/readme.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/',
                                   {'person': '2', 'file': fp}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 1)
        self.assertEqual(Attachment.objects.all()[0].pk, 1)

        # There is an issue with Client downloading MEDIA_ROOT files
        # then we only get URL, then open this file with PYTHON
        response_get = c.get('/candidate/attachment/get/1', follow=True)
        self.assertEquals(response_get.status_code, 404)

        file_path = response_get.redirect_chain[0][0][len(
            "http://testserver/"):]
        self.verify_file_content(file_path)

        # Add second file to same person
        self.assertEqual(len(Attachment.objects.all()), 1)
        with open(BASE_DIR +
                  '/power_recruiter/tests/upload_files/list.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/',
                                   {'person': '3', 'file': fp}, follow=True)

        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 2)
        self.assertEqual(Attachment.objects.all()[0].pk, 1)
        self.assertEqual(Attachment.objects.all()[1].pk, 2)

        # Remove first file
        c.post('/candidate/attachment/remove/', {'id': 1}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 1)
        self.assertEqual(Attachment.objects.all()[0].pk, 2)
        self.assertEqual("list",
                         str(Attachment.objects.all()[0])[:len("list")])

        # It's safe remove after all
        self.verify_file_content(file_path)

    @override_settings(DEBUG=True)
    def test_attachment_remove_404(self):
        c = Client(enforce_csrf_checks=False)
        response_remove = c.post('/candidate/attachment/remove/', {'id': 1},
                                 follow=True)
        self.assertEqual(response_remove.status_code, 404)
        response_remove = c.post('/candidate/attachment/remove/', {},
                                 follow=True)
        self.assertEqual(response_remove.status_code, 404)

    @override_settings(DEBUG=True)
    def test_change_name(self):
        c = Client(enforce_csrf_checks=False)
        kamila = Person.objects.get(pk=2)
        self.assertEqual(kamila.first_name, "Kamila")
        self.assertEqual(kamila.last_name, "Kruk")
        response_post = c.post(
            '/candidate/change_name/',
            {'id': 2, 'name': 'Kamilsha von Kruk - Kowalska'},
            follow=True)
        self.assertEqual(response_post.status_code, 200)
        kamila = Person.objects.get(pk=2)
        self.assertEqual(kamila.first_name, "Kamilsha")
        self.assertEqual(kamila.last_name, "von Kruk - Kowalska")

    @override_settings(DEBUG=True)
    def test_change_name_404(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post('/candidate/change_name/',
                               {'id': 8, 'name': 'A A'}, follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post('/candidate/change_name/', {'name': 'A A'},
                               follow=True)
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_remove_person(self):
        c = Client(enforce_csrf_checks=False)
        self.assertEqual(len(Person.objects.all()), 6)
        self.assertNotEqual(Person.objects.get(pk=1), None)
        response_remove = c.post('/candidate/remove/', {'id': 1}, follow=True)
        self.assertEqual(response_remove.status_code, 200)
        self.assertEqual(len(Person.objects.all()), 5)

        try:
            not_exist = Person.objects.get_object_or_None(pk=1)
        except:
            not_exist = None
        self.assertEqual(not_exist, None)

    @override_settings(DEBUG=True)
    def test_person_remove_404(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post('/candidate/remove/', {'id': 9}, follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post('/candidate/remove/', {}, follow=True)
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_candidate_json(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post('/candidate/')
        candidates = json.loads(response_post.content)
        self.assertEqual(len(candidates), 6)

        first_candidate = candidates[0]

        # photo and notifications
        correct_photo = {
            "photo": '',
            "notifications": [
                {"message": u"Co\u015b za d\u0142ugo nie ma spotkania"}
            ]
        }
        self.assertEqual(first_candidate["photo"], correct_photo)

        # id
        self.assertEqual(first_candidate["id"]["id"], 1)

        # name
        correct_name = {
            "candidate_name": "Krzysztof Fudali",
            "candidate_id": 1
        }
        self.assertEqual(first_candidate["candidate_name"], correct_name)

        # contact
        correct_contact = {
            "candidate_name": "Krzysztof Fudali",
            "email": None,
            "candidate_id": 1,
            "linkedin": None,
            "goldenline": None
        }
        self.assertEqual(first_candidate["contact"], correct_contact)

        # state
        self.assertEqual(
            first_candidate["state"]["raw_state_name"],
            "First meeting")

        # state history
        self.assertEquals(len(first_candidate["state"]["state_history"]), 5)
        last_state = first_candidate["state"]["state_history"][0]
        self.assertEquals(last_state["start_date"], "2014-12-21")
        self.assertEquals(last_state["change_date"], "2014-12-31")
        self.assertTrue("Positive response" in last_state["state"])

        # attachments
        correct_attachments = {"candidate_id": 1, "attachments": []}
        self.assertEqual(first_candidate["attachments"], correct_attachments)

        # caveats
        correct_caveats = {
            "candidate_name": "Krzysztof Fudali",
            "caveats": "Good programmer!",
            "candidate_id": 1
        }
        self.assertEqual(first_candidate["caveats"], correct_caveats)

    @override_settings(DEBUG=True)
    def test_candidate_json_filtration(self):
        c = Client()
        response = c.get("/candidate/?dummy=1&state2=0&state10=0")
        candidates = json.loads(response.content)
        self.assertEqual(len(candidates), 3)

    @override_settings(DEBUG=True)
    def test_caveats(self):
        c = Client()
        candidate = Person.objects.get(pk=1)
        self.assertEqual(candidate.caveats, "Good programmer!")
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'id': 1, 'timestamp': int(float(time.time()) * 1000),
             'caveats': "New caveats ;)"},
            follow=True)
        self.assertEqual(response_post.status_code, 200)
        candidate = Person.objects.get(pk=1)
        self.assertEqual(candidate.caveats, "New caveats ;)")
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'id': 1, 'timestamp': int(float(time.time()) * 1000 - 2000),
             'caveats': "Old caveats ;)"},
            follow=True)
        self.assertEqual(response_post.status_code, 200)
        candidate = Person.objects.get(pk=1)
        self.assertEqual(candidate.caveats, "New caveats ;)")

    @override_settings(DEBUG=True)
    def test_caveats_404(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'timestamp': int(float(time.time()) * 1000),
             'caveats': "New caveats ;)"},
            follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'id': 1, 'caveats': "New caveats ;)"},
            follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'id': 1, 'timestamp': int(float(time.time()) * 1000 - 2000)},
            follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post(
            '/candidate/caveats/upload/',
            {'id': 0, 'timestamp': int(float(time.time()) * 1000 - 2000),
             'caveats': "Old caveats ;)"},
            follow=True)
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_change(self):
        c = Client(enforce_csrf_checks=False)
        candidate = Person.objects.get(pk=4)
        self.assertEqual(candidate.state.pk, 4)
        state_history = OldState.objects.filter(
            person_id=candidate.pk).order_by('-change_date').all()
        self.assertEqual(len(state_history), 2)

        response_post = c.post(
            '/candidate/change_state/', {'person_id': 4, 'new_state_id': 2},
            follow=True)
        self.assertEqual(response_post.status_code, 200)
        candidate = Person.objects.get(pk=4)
        self.assertEqual(candidate.state.pk, 2)
        self.assertEqual(len(OldState.objects.filter(person_id=candidate.pk)),
                         3)

        new_state_history = OldState.objects.filter(
            person_id=candidate.pk).order_by('-change_date').all()
        last_state = new_state_history[0]
        self.assertEqual(last_state.state.pk, 4)
        self.assertEqual(last_state.start_date.date(),
                         datetime.date(2014, 12, 23))
        self.assertEqual(last_state.change_date.date(),
                         datetime.datetime.now().date())
        self.assertEqual(new_state_history[1], state_history[0])
        self.assertEqual(new_state_history[2], state_history[1])

    @override_settings(DEBUG=True)
    def test_change_404(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post('/candidate/change_state/',
                               {'person_id': 4, 'new_state_id': 3},
                               follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post('/candidate/change_state/',
                               {'person_id': 7, 'new_state_id': 3},
                               follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post('/candidate/change_state/', {'person_id': 4},
                               follow=True)
        self.assertEqual(response_post.status_code, 404)
        response_post = c.post('/candidate/change_state/', {'new_state_id': 3},
                               follow=True)
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_add_from_app(self):
        c = Client(enforce_csrf_checks=False)
        self.assertEqual(len(Person.objects.all()), 6)
        response_post = c.post('/candidate/add_from_app', {
            'first_name': 'Nowy',
            'last_name': 'Kandydat',
            'goldenline_link': 'http://goldenline.com/test',
            'linkedin_link': 'http://linkedin.com/test',
            'email_link': 'test@powerrecruiter-zpp.pl'
        })
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Person.objects.all()), 7)

        candidate = Person.objects.get(pk=7)
        self.assertEqual(candidate.first_name, "Nowy")
        self.assertEqual(candidate.last_name, "Kandydat")
        self.assertEqual(candidate.current_state_started.date(),
                         datetime.datetime.now().date())
        self.assertEqual(candidate.state.pk, 0)
        self.assertEqual(candidate.photo_url, "")
        self.assertEqual(candidate.linkedin, 'http://linkedin.com/test')
        self.assertEqual(candidate.goldenline, 'http://goldenline.com/test')
        self.assertEqual(candidate.email, 'test@powerrecruiter-zpp.pl')
        self.assertEqual(candidate.caveats, "")
        self.assertEqual(candidate.caveats_timestamp.date(),
                         datetime.datetime.now().date())

    @override_settings(DEBUG=True)
    def test_add_from_app_404(self):
        c = Client(enforce_csrf_checks=False)
        response_post = c.post('/candidate/add_from_app', {
            'last_name': 'Kandydat',
            'goldenline_link': 'http://goldenline.com/test',
            'linkedin_link': 'http://linkedin.com/test',
            'email_link': 'test@powerrecruiter-zpp.pl'
        })
        self.assertEqual(response_post.status_code, 404)

        response_post = c.post('/candidate/add_from_app', {
            'first_name': 'Nowy',
            'goldenline_link': 'http://goldenline.com/test',
            'linkedin_link': 'http://linkedin.com/test',
            'email_link': 'test@powerrecruiter-zpp.pl'
        })
        self.assertEqual(response_post.status_code, 404)

        response_post = c.post('/candidate/add_from_app', {
            'first_name': 'Nowy',
            'last_name': 'Kandydat',
            'linkedin_link': 'http://linkedin.com/test',
            'email_link': 'test@powerrecruiter-zpp.pl'
        })
        self.assertEqual(response_post.status_code, 404)

        response_post = c.post('/candidate/add_from_app', {
            'first_name': 'Nowy',
            'last_name': 'Kandydat',
            'goldenline_link': 'http://goldenline.com/test',
            'email_link': 'test@powerrecruiter-zpp.pl'
        })
        self.assertEqual(response_post.status_code, 404)

        response_post = c.post('/candidate/add_from_app', {
            'first_name': 'Nowy',
            'last_name': 'Kandydat',
            'goldenline_link': 'http://goldenline.com/test',
            'linkedin_link': 'http://linkedin.com/test',
        })
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_browser_plugin_mockup(self):
        c = Client(enforce_csrf_checks=False)
        self.assertEqual(len(Person.objects.all()), 6)

        # Add goldenline
        response_post = c.post('/candidate/add', {
            'args[0]': 'Nowy Kandydat',
            'args[1]': 'http://nofoto.com/photo.png',
            'args[2]': 'http://goldenline.com/test'
        })
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Person.objects.all()), 7)

        candidate = Person.objects.get(pk=7)
        self.assertEqual(candidate.first_name, "Nowy")
        self.assertEqual(candidate.last_name, "Kandydat")
        self.assertEqual(candidate.current_state_started.date(),
                         datetime.datetime.now().date())
        self.assertEqual(candidate.state.pk, 0)
        self.assertEqual(candidate.photo_url, "http://nofoto.com/photo.png")
        self.assertEqual(candidate.linkedin, None)
        self.assertEqual(candidate.goldenline, "http://goldenline.com/test")
        self.assertEqual(candidate.email, None)
        self.assertEqual(candidate.caveats, "")
        self.assertEqual(candidate.caveats_timestamp.date(),
                         datetime.datetime.now().date())

        # Add goldenline second time
        response_post = c.post('/candidate/add', {
            'args[0]': 'Nowy Kandydat',
            'args[1]': 'http://nofoto.com/photo.png',
            'args[2]': 'http://goldenline.com/test'
        })
        self.assertEqual(response_post.status_code, 418)

        # Add linkedin
        response_post = c.post('/candidate/add', {
            'args[0]': 'Kamil Linkinowiec',
            'args[1]': 'http://nofoto.com/photo.png',
            'args[2]': 'http://linkedin.com/test'
        })
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Person.objects.all()), 8)
        candidate = Person.objects.get(pk=8)
        self.assertEqual(candidate.linkedin, "http://linkedin.com/test")
        self.assertEqual(candidate.goldenline, None)
        self.assertEqual(candidate.email, None)

        # Add linkedin second time
        response_post = c.post('/candidate/add', {
            'args[0]': 'Kamil Linkinowiec',
            'args[1]': 'http://nofoto.com/photo.png',
            'args[2]': 'http://linkedin.com/test'
        })
        self.assertEqual(response_post.status_code, 418)

    @override_settings(DEBUG=True)
    def test_browser_plugin_mockup_404(self):
        c = Client(enforce_csrf_checks=False)

        # Add goldenline
        response_post = c.post('/candidate/add', {
            'args[3]': 'Nowy Kandydat',
            'args[1]': 'http://nofoto.com/photo.png',
            'args[2]': 'http://goldenline.com/test'
        })
        self.assertEqual(response_post.status_code, 404)

    @override_settings(DEBUG=True)
    def test_get_conflicts(self):
        c = Client(enforce_csrf_checks=False)
        response = c.get('/candidate/get_conflicts/')
        self.assertEqual(response.status_code, 200)
        conflicts = json.loads(response.content)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(len(conflicts[0]), 0)

        new_person1 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama"
        )
        new_person1.save()

        new_person2 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama",
            linkedin="http://www.linkedin.com/costam2",
            photo_url="http://japonskie_twarze.pl/taka_sama.png"
        )
        new_person2.save()

        response = c.get('/candidate/get_conflicts/')
        self.assertEqual(response.status_code, 200)
        conflicts = json.loads(response.content)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(len(conflicts[0]), 2)

    @override_settings(DEBUG=True)
    def test_merge(self):
        c = Client(enforce_csrf_checks=False)
        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 0)
        self.assertEqual(len(Person.objects.all()), 6)
        new_person1 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama"
        )
        new_person1.save()

        new_person2 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama",
            linkedin="http://www.linkedin.com/costam2",
            photo_url="http://japonskie_twarze.pl/taka_sama.png"
        )
        new_person2.save()

        # caveats should concat
        candidate1 = Person.objects.get(pk=7)
        candidate1.caveats = "2+2="
        candidate1.save()

        candidate2 = Person.objects.get(pk=8)
        candidate2.caveats = "2*2"
        candidate2.save()

        # attachments should concat!
        with open(BASE_DIR +
                  '/power_recruiter/tests/upload_files/readme.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/',
                                   {'person': '7', 'file': fp}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 1)

        # Add second file to same person
        self.assertEqual(len(Attachment.objects.all()), 1)
        with open(BASE_DIR +
                  '/power_recruiter/tests/upload_files/list.txt') as fp:
            response_post = c.post('/candidate/attachment/upload/',
                                   {'person': '8', 'file': fp}, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(len(Attachment.objects.all()), 2)

        self.assertEqual(len(Person.objects.all()), 8)

        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 2)
        response_post = c.post('/candidate/resolve_conflicts/',
                               {'ids': '[7,8]', 'img': 1, 'state': 1,
                                'merge': 'true'})
        self.assertEqual(response_post.status_code, 200)

        self.assertEqual(len(Person.objects.all()), 7)

        candidate = Person.objects.get(pk=7)
        self.assertEqual(candidate.first_name, "Taka")
        self.assertEqual(candidate.last_name, "Sama")
        self.assertEqual(candidate.current_state_started.date(),
                         datetime.datetime.now().date())
        self.assertEqual(candidate.state.pk, 0)
        self.assertEqual(candidate.photo_url,
                         "http://japonskie_twarze.pl/taka_sama.png")
        self.assertEqual(candidate.linkedin, None)
        self.assertEqual(candidate.goldenline, None)
        self.assertEqual(candidate.email, None)
        self.assertEqual(candidate.caveats, "2+2=2*2")
        self.assertEqual(candidate.caveats_timestamp.date(),
                         datetime.datetime.now().date())
        self.assertEqual(len(Attachment.objects.all().filter(person=7)), 2)

        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 0)

    @override_settings(DEBUG=True)
    def test_dont_merge(self):
        c = Client(enforce_csrf_checks=False)
        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 0)
        self.assertEqual(len(Person.objects.all()), 6)
        new_person1 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama"
        )
        new_person1.save()

        new_person2 = Person.objects.create_person(
            first_name="Taka",
            last_name="Sama",
            linkedin="http://www.linkedin.com/costam2",
            photo_url="http://japonskie_twarze.pl/taka_sama.png"
        )
        new_person2.save()

        self.assertEqual(len(Person.objects.all()), 8)
        all_people_list = Person.objects.all()

        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 2)
        response_post = c.post('/candidate/resolve_conflicts/',
                               {'ids': '[7,8]', 'img': 0, 'state': 0,
                                'merge': 'false'})
        self.assertEqual(response_post.status_code, 200)

        new_all_people_list = Person.objects.all()
        self.assertEqual(len(all_people_list), len(new_all_people_list))
        for i in xrange(len(all_people_list)):
            self.assertEqual(all_people_list[i], new_all_people_list[i])

        conflicts = Person.get_conflicts()
        self.assertEqual(len(conflicts), 0)
