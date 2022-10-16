from django.db import models
from django.views.generic.detail import DetailView


class Department(models.Model):
    """
    Model that describes a whole department.
    """
    slug = models.SlugField(max_length=10, null=True)
    
    def __str__(self):
        return self.subject
    
class Course(Department):
    """
    Model that visualizes a specific course in a department.
    This model inherits from the Department model.
    """
    
    # Instructor Logistics
    instructor_name = models.CharField(max_length=120)
    instructor_email = models.CharField(max_length=60)
    
    
    # Course Logistics
    semester_code = models.CharField(max_length=20)
    course_num = models.CharField(max_length=20)
    course_name = models.CharField(max_length=150)
    section = models.CharField(max_length=5)
    capacity = models.CharField(max_length=20)
    location = models.CharField(max_length=70)
    
    # Course Timing Logistics
    meeting_days = models.CharField(max_length=20)
    start_time = models.CharField(max_length=30)
    end_time = models.CharField(max_length=30)
    
    def __str__(self):
        # EX: CS1110 -- 001: Introduction to Programming
        return self.subject + self.course_num + " -- " + self.section + ": " + self.course_name
    
class CourseDetail(DetailView):
    model = Course
    
    
    
    
    
    
    