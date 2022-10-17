from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course
import requests

# Create your views here.
#@csrf_exempt
def index(request):
    return HttpResponse("Welcome to the better Lou's List!")

#@csrf_exempt
def login(request):

    d = Department.objects.all().order_by('slug')
    all_departments = {
        "department": d
    }
    
    # Checks if the database has values in it.
    # If not, update the database.
    if not d:
        all_departments = {}
        url = "http://luthers-list.herokuapp.com/api/deptlist"
        response = requests.get(url)
        data = response.json()   
        subjects = data
        for s in subjects:
            department = Department(slug = s['subject'])
            department.save()
            
            c = Course.objects.all().filter(slug=department.slug)    
            if not c:
                course_url = "http://luthers-list.herokuapp.com/api/dept/" + str(department.slug) + "/"
                print(course_url)
                course_response = requests.get(course_url)
                course_data = course_response.json()
                courses = course_data
                for c in courses:
                    if len(c['meetings']) > 0:
                        course = Course(
                            instructor_name = c['instructor']['name'],
                            instructor_email = c['instructor']['email'],
                            semester_code = c['semester_code'],
                            course_num = c['catalog_number'],
                            course_name = c['description'],
                            section = c['course_section'],
                            capacity = c['class_capacity'],
                                    
                            location = c['meetings'][0]['facility_description'],
                            meeting_days = c['meetings'][0]['days'],
                            start_time = c['meetings'][0]['start_time'],
                            end_time = c['meetings'][0]['end_time'],
                        )
                    else:
                        course = Course(
                            instructor_name = c['instructor']['name'],
                            instructor_email = c['instructor']['email'],
                            semester_code = c['semester_code'],
                            course_num = c['catalog_number'],
                            course_name = c['description'],
                            section = c['course_section'],
                            capacity = c['class_capacity'],
                                    
                            location = "--",
                            meeting_days = "--",
                            start_time = "--",
                            end_time = "--",
                        )                        
                    course.save()
                
        # Re-grab the departments to show
        d = Department.objects.all().order_by('slug')
        all_departments = {
            "department": d
        }
            
    return render(request, 'app.html', all_departments)


class DepartmentView(DetailView):
    model = Department
    template_name = "class.html"
    # Update courses database

            
        
        
