from django.test import TestCase
from django.test import Client
import unittest
from app.models import Department, Course, CourseDetail

# Create your tests here.
class YourTestClass(TestCase):
        # def test_view_url_exists_at_desired_location(self):
        #         response = self.client.get('')
        #         self.assertEqual(response.status_code, 200)
        def test_view_url_exists_at_second_location(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)

class TestModels(TestCase):
        def DepartmentStr(self):
                dept = Department.objects.create(slug="PHIL")
                self.assertEqual(str(dept),"PHIL")

