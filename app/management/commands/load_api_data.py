
from app.models import Department, Course
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):

        url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228"
        response = requests.get(url)
        data = response.json()   
        subjects = data['subjects']

        for subject in subjects:
            
            current_department = Department(slug=subject['subject'])

            #Search database to check if it already exists
            d = Department.objects.all().filter(slug = current_department.slug)
            if(not d):
        
                current_department.save()
                    
                #this code will find all of the courses for every department

                #course_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=CS&page=1" + str(current_department.slug) + "/"
                course_url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=" + str(current_department.slug) + "&page=1"
                course_response = requests.get(course_url)
                course_data = course_response.json()
                
                # for course in course_data:
                #     print(course['instructors'][0]['name'])



                courses = course_data
                for c in courses:
                    try:
                        if len(c['meetings'][0]) > 0:
                            course = Course(
                        
                            department_ptr = current_department,
                            dept_slug = current_department.slug,
                            instructor_name = c['instructors'][0]['name'],
                            instructor_email = c['instructors'][0]['email'],
                            course_num = c['class_nbr'],
                            semester_code = c['strm'][3],
                            section = c['class_section'],
                            subject = c['subject'],
                            course_cat = c['catalog_nbr'],
                            course_name = c['descr'],
                            units = c['units'],
                            component = c['component'],
                            capacity = c['class_capacity'],
                            wait_list = c['wait_tot'],
                            wait_cap = c['wait_cap'],
                            enrollment_total = c['enrollment_total'],
                            enrollment_available = c['enrollment_available'],
                            topic  = c['topic'],

                            location = c['location'],
                            meeting_days = c['meetings'][0]['days'],
                            start_time = c['meetings'][0]['start_time'][0:2]+":"+c['meetings'][0]['start_time'][3:5],
                            end_time = c['meetings'][0]['end_time'][0:2]+":"+c['meetings'][0]['end_time'][3:5],
                            )
                    except:
                        course = Course(
                    
                        department_ptr = current_department,
                        dept_slug = current_department.slug,
                        instructor_name = c['instructors'][0]['name'],
                        instructor_email = c['instructors'][0]['email'],
                        course_num = c['class_nbr'],
                        semester_code = c['strm'][3],
                        section = c['class_section'],
                        subject = c['subject'],
                        course_cat = c['catalog_nbr'],
                        course_name = c['descr'],
                        units = c['units'],
                        component = c['component'],
                        capacity = c['class_capacity'],
                        wait_list = c['wait_tot'],
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