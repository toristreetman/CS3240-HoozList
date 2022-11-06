from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course
import requests
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q

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
    return render(request, 'profile.html')

def SearchView(request):
    template_name = "search_view.html"
    if request.method == "POST":
        searched = request.POST['searched']
        courses = Course.objects.filter(Q(course_name__icontains = searched)|Q(section__icontains = searched)
        |(Q(subject__istartswith = searched)& Q(subject__iendswith = searched))|Q(course_cat__icontains = searched)|(Q(subject__icontains = searched)&Q(course_cat__icontains = searched))|Q(instructor_name__icontains = searched)
        |Q(meeting_days__icontains = searched)|Q(start_time__icontains = searched)|Q(end_time__icontains = searched)|Q(location__icontains = searched))
        return render(request, 'search_view.html',{'searched': searched, 'courses': courses})
    else:
        return render(request, 'search_view.html')

