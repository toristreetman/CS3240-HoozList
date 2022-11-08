from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course
import requests
from django.views import generic
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required     
def ProfileView(request):
   # if not request.user.is_authenticated:
      #  return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        #return render(request, "profile_not_logged_in.html")

    saved_courses_list = request.user.userprofile.saved_courses.all()
    scheduled_courses_list = request.user.userprofile.scheduled_courses.all()
    friends_list = request.user.userprofile.friends.all()
    

    return render(request, 'profile.html', {
                                            'saved_courses_list': saved_courses_list, 
                                            'scheduled_courses_list': scheduled_courses_list,
                                            'friends_list': friends_list})
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

    dictionary = {"success": True, "msg": "Course Saved Successfully" }
    #return render(request,'saved_courses.html',{'user' : user_saving, 'course' :course_to_save})
    messages.success(request, "Your course has been saved!")
    return HttpResponseRedirect(reverse('courses', args=(slug,)))

def SaveCourseInSchedule(request, slug):
    # access course based on request ID
    selected_course = get_object_or_404(Course, pk=request.POST['course_choice']) 
    course_to_save = vars(selected_course)

    # access user courses and information
    user_info = request.user
    user_courses = request.user.userprofile.scheduled_courses.all()

    # If course is asynchronous, then just add it regardless
    if len(course_to_save['start_time']) < 10:
        user_info.userprofile.scheduled_courses.add(selected_course)
        return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})
        
    start_time = int(course_to_save['start_time'][:2] + course_to_save['start_time'][3:5])
    end_time = int(course_to_save['end_time'][:2] + course_to_save['end_time'][3:5])
    
    # see if there are any course conflicts
    # if any conflict: return an error page
    # else: add the course to schedule
    for saved_course in user_courses:
        dict_saved_course = vars(saved_course)
        
        
        # Check if there is no time, then just add the course regardless
        if len(dict_saved_course['start_time']) < 10:
            continue
        
        comp_start_time = int(dict_saved_course['start_time'][:2] + dict_saved_course['start_time'][3:5]) 
        comp_end_time = int(dict_saved_course['end_time'][:2] + dict_saved_course['end_time'][3:5]) 
        if start_time >= comp_start_time and start_time <= comp_end_time:
            return render(request, 'course_schedule_error.html', 
                          {'user' : user_info, 
                          'conflicted_course': saved_course,
                          'selected_course': course_to_save})
            
        elif end_time >= comp_start_time and end_time <= comp_end_time:
            return render(request, 'course_schedule_error.html', 
                          {'user' : user_info, 
                          'conflicted_course': saved_course,
                          'selected_course': selected_course}) 
    
    user_info.userprofile.scheduled_courses.add(selected_course)
    return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})

def DeleteCourse(request):
    selected_course = get_object_or_404(Course, pk=request.POST['course_choice'])
    
    user_courses = request.user.userprofile.saved_courses.all()
    user_info = request.user
    
    # Ensure that the selected_course is within the user_courses
    if selected_course in user_courses:
        user_info.userprofile.saved_courses.remove(selected_course)
        messages.success(request, "Your course has been deleted!")
        return HttpResponseRedirect('/profile/')
        #return render(request, 'delete_save.html', {'user' : user_info, 'course': selected_course})
    
    # Somehow selected course that was not in user list, so return an error page
    else:
        return render(request, 'error.html')
    
def DeleteScheduledCourse(request):
    selected_course = get_object_or_404(Course, pk=request.POST['course_choice'])
    
    user_courses = request.user.userprofile.scheduled_courses.all()
    user_info = request.user
    
    # Ensure that the selected_course is within the user_courses
    if selected_course in user_courses:
        user_info.userprofile.scheduled_courses.remove(selected_course)
        return render(request, 'delete_schedule.html', {'user' : user_info, 'course': selected_course})
    
    # Somehow selected course that was not in user list, so return an error page
    else:
        return render(request, 'error.html')
