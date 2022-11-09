
from app.models import Department, Course
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):
            url = "http://luthers-list.herokuapp.com/api/deptlist"
            response = requests.get(url)
            data = response.json()   
            subjects = data
            for s in subjects:
                 # Make department object
                current_department = Department(slug = s['subject'])

                #Search database to check if it already exists
                d = Department.objects.all().filter(slug = current_department.slug)
                if(not d):
                
                    current_department.save()
                        
                
                    course_url = "http://luthers-list.herokuapp.com/api/dept/" + str(current_department.slug) + "/"
                    print(course_url)
                    course_response = requests.get(course_url)
                    course_data = course_response.json()
                    courses = course_data
                    for c in courses:
                        if len(c['meetings']) > 0:
                            course = Course(
                            
                            department_ptr = current_department,
                            dept_slug = current_department.slug,
                            instructor_name = c['instructor']['name'],
                            instructor_email = c['instructor']['email'],
                            course_num = c['course_number'],
                            semester_code = c['semester_code'],
                            section = c['course_section'],
                            subject = c['subject'],
                            course_cat = c['catalog_number'],
                            course_name = c['description'],
                            units = c['units'],
                            component = c['component'],
                            capacity = c['class_capacity'],
                            wait_list = c['wait_list'],
                            wait_cap = c['wait_cap'],
                            enrollment_total = c['enrollment_total'],
                            enrollment_available = c['enrollment_available'],
                            topic  = c['topic'],

                                                
                            location = c['meetings'][0]['facility_description'],
                            meeting_days = c['meetings'][0]['days'],
                            start_time = c['meetings'][0]['start_time'][0:2]+":"+c['meetings'][0]['start_time'][3:5],
                            end_time = c['meetings'][0]['end_time'][0:2]+":"+c['meetings'][0]['end_time'][3:5],
                            )
                        else:
                            course = Course(
                            
                            department_ptr = current_department,
                            instructor_name = c['instructor']['name'],
                            instructor_email = c['instructor']['email'],
                            course_num = c['course_number'],
                            semester_code = c['semester_code'],
                            section = c['course_section'],
                            subject = c['subject'],
                            course_cat = c['catalog_number'],
                            course_name = c['description'],
                            units = c['units'],
                            component = c['component'],
                            capacity = c['class_capacity'],
                            wait_list = c['wait_list'],
                            wait_cap = c['wait_cap'],
                            enrollment_total = c['enrollment_total'],
                            enrollment_available = c['enrollment_available'],
                            topic  = c['topic'],
                                                
                            location = "--",
                            meeting_days = "--",
                            start_time = "--",
                            end_time = "--",
                            
                            )                        
                        course.save()