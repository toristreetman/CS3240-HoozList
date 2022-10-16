from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import Department, Course
import requests
import pandas as pd

# Create your views here.
#@csrf_exempt
def index(request):
    return HttpResponse("Welcome to the better Lou's List!")

#@csrf_exempt
def login(request):

    d = Department.objects.all().order_by('subject')
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
            department = Department(subject = s['subject'])
            department.save()
        d = Department.objects.all().order_by('subject')
        all_departments = {
            "department": d
        }
            
    return render(request, 'app.html', all_departments)


def department(request):
    return render(request, 'class.html')
        
        
