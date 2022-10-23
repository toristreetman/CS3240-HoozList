from django.test import TestCase

# Create your tests here.
class YourTestClass(TestCase):
        def setUp(self):
                #Setup run before every test method
                pass
        def tearDown(self):
                #Clean up run after every test method
        def test_view_url_exists_at_desired_location(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)

