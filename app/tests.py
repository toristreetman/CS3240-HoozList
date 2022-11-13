from django.test import TestCase
from django.test import Client

import unittest
from app.models import Department, Course, UserProfile, Comment
from django.contrib.auth.models import User
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
    def test_departmentStr(self):
        dept = Department.objects.create(slug="PHIL")
        self.assertEqual(str(dept),"PHIL")

    def test_courseStr(self):
        co = Course.objects.create(subject="CS",
                                   course_cat="1110",
                                   section = "001",
                                   course_name="Introduction to Programming")
        self.assertEqual(str(co),"CS1110 -- 001: Introduction to Programming")

    def test_commentStr(self):
        comment = Comment.objects.create(comment="This is a test comment")
        self.assertEqual(str(comment), "This is a test comment")

    def userStr(self):
        user = User.objects.create(
                username="Mark",
                email="Mark@Sheriff.com",
                password="123"
                )
        profile = UserProfile.objects.create(user=user)

        self.assertEqual(str(profile), "Mark")


    # Check if the content in the log-in page is working correctly
    def test_view_log(self):
        response = self.client.get('')
        self.assertContains(response, "Log In")

    def test_view_hooz(self):
        response = self.client.get('')
        self.assertContains(response, "HoozList")

    # Check if dept-list website disallows user to view courses without being logged in
    def test_view_notloggedin(self):
        response = self.client.get('/dept-list/')
        self.assertContains(response, "Please sign in to access the course catalog!")
        response = self.client.get('/saved-friends/')
        self.assertContains(response, "Sign In")
        response = self.client.get('/sched-courses/')
        self.assertContains(response, "Sign In")
        response = self.client.get('/saved-courses/')
        self.assertContains(response, "Sign In")

        #Check if the search page functions
    def test_search_url(self):
        response = self.client.get('/search_view/')
        self.assertEqual(response.status_code, 200)

    #Check if the page contains the right words
    def test_view_notloggedin(self):
        response = self.client.get('/search_view/')
        self.assertContains(response, "Please type what you are looking for into the search bar!")


    #Check if the profile page has User information

    #Check if the profile page has Saved Course
    def user_add_course(self):
        co = Course.objects.create(
                subject="CS",
                course_num="1110",
                section = "001",
                course_name="Introduction to Programming"
                )
        user = User.objects.create(
                username="Mark",
                email="Mark@Sheriff.com",
                password="123"
                )

        profile = UserProfile.objects.create(user=user)
        profile.saved_courses.add(co)
        self.assertContains(profile.saved_courses, co)

    def user_add_course_sched(self):
        co = Course.objects.create(
                subject="CS",
                course_num="1110",
                section = "001",
                course_name="Introduction to Programming"
                )
        user = User.objects.create(
                username="Mark",
                email="Mark@Sheriff.com",
                password="123"
                )

        profile = UserProfile.objects.create(user=user)
        profile.scheduled_courses.add(co)
        self.assertContains(profile.scheduled_courses, co)

    #Check if the profile page has Your Schedule

    #Check if the profile page has Friends

    #Enter CS in the search bar, and CS1110 should be among the list

    #Enter Sherriff in the search bar, and CS3240 should be among the list

    #Many to many relationship model testing 
       
    



        




       


        




       

