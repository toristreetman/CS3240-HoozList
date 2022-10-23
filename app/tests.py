from django.test import TestCase
from django.test import Client

import unittest
from app.models import Department, Course, CourseDetail
from django.contrib.sites.models import Site
from django.db import models
from django.contrib import auth


class YourTestClass(TestCase):
        def test_view_url(self):
                response = self.client.get('')
                self.assertEqual(response.status_code, 200)
        def test_view_url_exists_at_second_location(self):
                response1 = self.client.get('/dept-list/')
                self.assertEqual(response1.status_code, 200)

# check if the two models that are essential to the first feature is working correctly

        def departmentStr(self):
                dept = Department.objects.create(slug="PHIL")
                self.assertEqual(str(dept),"PHIL")

        def courseStr(self):
                co = Course.objects.create(subject="CS",course_num="1110",section = "001",
                course_name="Introduction to Programming")
                self.assertEqual(str(co),"CS1110 -- 001: Introduction to Programming")
#Check if the content in the log-in page is working correctly
        def test_view_log(self):
                response = self.client.get('')
                self.assertContains(response, "Log In")
        def test_view_hooz(self):
                response = self.client.get('')
                self.assertContains(response, "HoozList")
#Check if dept-list website disallows user to view courses without being logged in
        def test_view_notloggedin(self):
                response = self.client.get('/dept-list/')
                self.assertContains(response, "Please sign in to access the course catalog!")

       
    



        




       

