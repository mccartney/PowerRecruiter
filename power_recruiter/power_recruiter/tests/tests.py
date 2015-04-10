import subprocess, time, urllib2, os
import django.test as unittest
from django.test.utils import override_settings
from power_recruiter.settings import BASE_DIR


class UrlsTest(unittest.TestCase):

    fixtures = ['admin.json', 'graph.json', 'required.json']

    def run_url(self, url, code=200):
        client = unittest.Client()
        response = client.get(url)
        self.assertEqual(response.status_code, code)

    def run_auto_login(self, url):
        client = unittest.Client()
        response = client.get('/admin', follow=True)
        correct_chain = [
            ('http://testserver/admin/', 301),
            ('http://testserver/admin/login/?next=/admin/', 302),
            ('http://testserver/admin/', 302)
        ]
        self.assertEqual(correct_chain, response.redirect_chain)
        response = client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_root(self):
        self.run_url("/")

    def test_pie_chart(self):
        self.run_url("/pieChart")

    def test_line_chart(self):
        self.run_url("/lineChart")

    def test_admin(self):
        self.run_auto_login("/admin")

    def test_admin_person(self):
        self.run_auto_login("/admin/candidate/person/")

    @override_settings(DEBUG=True)
    def test_404_debug(self):
        self.run_url("/ssssdfasdf", 404)

    @override_settings(DEBUG=False)
    # Show handler404
    def test_404(self):
        self.run_url("/ssssdfasdf", 200)


class WsgiTest(unittest.TestCase):

    def test_wsgi(self):
        FNULL = open(os.devnull, 'w')
        proc = subprocess.Popen([BASE_DIR + "/manage.py",  "runserver"], stdout=FNULL, stderr=FNULL)
        time.sleep(5)
        self.assertGreater(proc.pid, 0)
        response = urllib2.urlopen("http://127.0.0.1:8000/")
        self.assertEqual(response.getcode(), 200)
        proc.kill()

