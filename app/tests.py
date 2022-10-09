from django.test import TestCase

# Create your tests here.
class YourTestClass(TestCase):
        def test_view_url_exists_at_desired_location(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)

