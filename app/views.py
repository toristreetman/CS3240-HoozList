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

    # d = Department.objects.all().order_by('slug')
    # all_departments = {
    #     "department": d
    # }       
    return render(request, 'app.html')


class DepartmentView(DetailView):
    model = Department
    template_name = "class.html"
    # Update courses database

            
        
        
