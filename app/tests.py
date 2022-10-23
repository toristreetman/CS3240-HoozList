from django.test import TestCase
from django.test import Client
import unittest
from app.models import Department, Course, CourseDetail

# Create your tests here.
#check if the main page could be found
class YourTestClass(TestCase):
        def test_view_url_exists_at_desired_location(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)
        # def test_view_url_exists_at_second_location(self):
        #         response = self.client.get('dept-list/')
        #         self.assertEqual(response.status_code, 200)

#check if department model's to string method is working correctly
class TestModels(TestCase):
        def DepartmentStr(self):
                dept = Department.objects.create(slug="PHIL")
                self.assertEqual(str(dept),"PHIL")

        def Course(self):
                co = Course.objects.create(subject="CS",course_num="1110",section = "001",course_name="Introduction to Programming")
                self.assertEqual(str(co),"CS1110 -- 001: Introduction to Programming")



