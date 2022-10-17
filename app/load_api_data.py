from app.models import Department, Course
import requests

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
        current_department = Department(slug = s['subject'])
        current_department.save()
            
        c = Course.objects.all().filter(slug=current_department.slug)    
        if not c:
            course_url = "http://luthers-list.herokuapp.com/api/dept/" + str(current_department.slug) + "/"
            print(course_url)
            course_response = requests.get(course_url)
            course_data = course_response.json()
            courses = course_data
            for c in courses:
                if len(c['meetings']) > 0:
                    course = Course(
                        departments = current_department,
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
                        start_time = c['meetings'][0]['start_time'],
                        end_time = c['meetings'][0]['end_time'],
                    )
                else:
                    course = Course(
                        department = current_department,
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