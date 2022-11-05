from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course
import requests
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
#@csrf_exempt
def index(request):
    return HttpResponse("Welcome to the better Lou's List!")

#@csrf_exempt
def login(request):  
    return render(request, 'app.html')



def DepartmentView(request):
    d = Department.objects.all().order_by('slug')
    all_departments = {
        "department": d
    }
    return render(request, 'department_view.html', all_departments)

class CoursesView(generic.DetailView):
    template_name = "course_view.html"
    model = Department
        
def ProfileView(request):
    saved_courses_list = request.user.userprofile.saved_courses.all()

    return render(request, 'profile.html', {'saved_courses_list':saved_courses_list})

# read about forms and POST methods
# I found this article to be useful
# https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data
def SaveCourse(request, slug):

    #accessing POST data sent by user (name and value variables)
    #getting specific course based on its unique ID
    course_to_save = get_object_or_404(Course, pk=request.POST['course_choice'])

    user_saving = request.user

    #adding the course to the new UserProfile model 
    user_saving.userprofile.saved_courses.add(course_to_save)

    return render(request,'saved_courses.html',{'user' : user_saving, 'course' :course_to_save})
