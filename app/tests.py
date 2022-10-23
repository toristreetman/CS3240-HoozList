from django.test import TestCase

# Create your tests here.
class YourTestClass(TestCase):
        def setUpTestData(cls):
                print("setUpTestData: Run once to set up non-modified data for all class methods.")
                pass

        def setUp(self):
                print("setUp: Run once for every test method to setup clean data.")
                pass
        def test_view_url_exists_at_desired_location(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)

