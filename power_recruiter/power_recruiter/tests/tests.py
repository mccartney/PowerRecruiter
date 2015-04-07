import django.test as unittest
__author__ = 'shadowsword'

class UrlsTest(unittest.TestCase):

    fixtures = ['admin.json']

    def run_url(self, url):
        client = unittest.Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def run_auto_login(self, url):
        client = unittest.Client()
        response = client.get(url, follow=True)
        correct_chain = [
            ('http://testserver/admin/', 301),
            ('http://testserver/admin/login/?next=/admin/', 302),
            ('http://testserver/admin/', 302)
        ]
        self.assertEqual(correct_chain, response.redirect_chain)

    def test_root(self):
        self.run_url("/")

    def test_pie_chart(self):
        self.run_url("/pieChart")


    def test_line_chart(self):
        self.run_url("/lineChart")


    def test_admin(self):
        self.run_auto_login("/admin")