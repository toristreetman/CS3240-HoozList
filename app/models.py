from django.db import models
from django.conf import settings
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, AnonymousUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class Department(models.Model):
    """
    Model that describes a whole department.
    """
    slug = models.SlugField(max_length=10, null=True)
    
    def __str__(self):
        return self.slug
    def first_letter(self):
        return self.slug and self.slug[0] or ''
    
class Course(models.Model):
    """
    Model that visualizes a specific course in a department.

    """
    #Key to link a course to a department
    department_ptr = models.ForeignKey(Department,on_delete=models.CASCADE, null=True)
    dept_slug = models.CharField(max_length=15, null=True)

    # Instructor Logistics
    instructor_name = models.CharField(max_length=120, null=True)
    instructor_email = models.CharField(max_length=60, null=True)
    
    
    # Course Logistics
    course_num = models.CharField(max_length=20, null=True)
    semester_code = models.CharField(max_length=20, null=True)
    section = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=20, null=True)
    course_cat = models.CharField(max_length=20, null=True)
    course_name = models.CharField(max_length=1200, null=True)
    units  = models.CharField(max_length=20, null=True)
    component = models.CharField(max_length=20, null=True)
    capacity = models.CharField(max_length=20, null=True)
    wait_list = models.CharField(max_length=20, null=True)
    wait_cap = models.CharField(max_length=20, null=True)
    enrollment_total = models.CharField(max_length=20, null=True)
    enrollment_available = models.CharField(max_length=20, null=True)
    topic = models.CharField(max_length=100, null=True)
    
    location = models.CharField(max_length=70, null=True)
    
    # Course Timing Logistics
    meeting_days = models.CharField(max_length=20, null=True)
    start_time = models.CharField(max_length=30, null=True)
    end_time = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        # EX: CS1110 -- 001: Introduction to Programming
        return self.subject + self.course_cat + " -- " + self.section + ": " + self.course_name
    

class Comment(models.Model):
    """
    Model that defines a comment on a user's schedule page.
    """
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    """
    Separate model that extends the Django User model using a 1-to-1 key.
    It has additional fields to keep track of courses, friends, comments, and much more.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank =True)
    scheduled_courses = models.ManyToManyField(Course, related_name='user_schedule')
    saved_courses = models.ManyToManyField(Course)
    friends = models.ManyToManyField(User, related_name='friends')
    comments_sent = models.ManyToManyField(Comment, related_name='comments_sent')
    comments_received = models.ManyToManyField(Comment, related_name='comments_received')

    major = models.CharField(max_length=60, null=True)
    year = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


# this receiver detects whenever a user is created with the default django User model
# and creates a UserProfile associated with that user
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    
    


    
