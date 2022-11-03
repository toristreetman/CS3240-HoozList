from django.db import models
from django.conf import settings
from django.views.generic.detail import DetailView


class Department(models.Model):
    """
    Model that describes a whole department.
    """
    slug = models.SlugField(max_length=10, null=True)
    
    def __str__(self):
        return self.subject
    
class Course(models.Model):
    """
    Model that visualizes a specific course in a department.

    """
    #Key to link a course to a department
    department_ptr = models.ForeignKey(Department,on_delete=models.CASCADE, null=True)

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
    topic  = models.CharField(max_length=100, null=True)
    
    location = models.CharField(max_length=70, null=True)
    
    # Course Timing Logistics
    meeting_days = models.CharField(max_length=20, null=True)
    start_time = models.CharField(max_length=30, null=True)
    end_time = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        # EX: CS1110 -- 001: Introduction to Programming
        return self.subject + self.course_num + " -- " + self.section + ": " + self.course_name
    
    
    
    
    
    
    