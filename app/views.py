from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course
import requests
from django.views import generic

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
        
        
