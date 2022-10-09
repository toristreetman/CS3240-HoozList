from django.test import TestCase
from django.urls import reverse

def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

def test_view_url_accounts_exists_at_desired_location(self):
        response = self.client.get('accounts/')
        self.assertEqual(response.status_code, 200)