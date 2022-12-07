from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from app.models import Department, Course, Comment
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

def userSettings(request):
    return render(request, 'userSettings_view.html')

def userSettingsUpdate(request):

    name = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    major = request.POST['major']
    year = request.POST['year']
    
    if name != "":
        request.user.first_name = name
    
    if lastname != "":
        request.user.last_name = lastname
    
    if username != "":
        request.user.username = username

    if major != "":
        request.user.userprofile.major = major
    
    if year != "":
        request.user.userprofile.year = year

    print(request.user.userprofile.major)
    messages.success(request, "Your profile has been updated!")
   

    
    request.user.save()
    request.user.userprofile.save()
    #print(year)
    return render(request, 'userSettings_view.html')

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
    

    return render(request, 'profile.html', {'saved_courses_list': saved_courses_list, 
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

###################### Friends ##############################
@login_required
def SavedFriendsView(request):
    friends_list = request.user.userprofile.friends.all()
    return render(request, 'saved_friends.html', {'friends_list': friends_list,})

@login_required
def SearchFriendView(request):
    if request.method == "POST":
        searched = request.POST['searched']
        friends = User.objects.filter(Q(first_name__icontains = searched)|Q(last_name__icontains = searched)
        |Q(email__istartswith = searched))
        friends_list = request.user.userprofile.friends.all()
        return render(request, 'saved_friends.html',{
            'searched': searched, 
            'friends': friends,
            'friends_list': friends_list,
            })
    else:
        return render(request, 'profile.html')

@login_required
def SaveFriend(request):
    try:
        friend_to_save = get_object_or_404(User, pk=request.POST['friend_choice'])
    except:
        return render(request, 'error.html')

    user_saving = request.user

    #adding the course to the new UserProfile model 
    user_saving.userprofile.friends.add(friend_to_save)
    messages.success(request, "Your friend has been added!")
    return HttpResponseRedirect('/saved-friends')

@login_required
def DeleteFriend(request):
     # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path()
    #print(incoming_url)
    split_url = incoming_url.split('/')
    #print(split_url)
    redirect_url = ""
    if split_url[1] == 'saved-friends':
        redirect_url = '/saved-friends/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'
    try:
        selected_friend = get_object_or_404(User, pk=request.POST['friend_choice'])
    except:
        return render(request, 'error.html')
    
    user_friends = request.user.userprofile.friends.all()
    user_info = request.user
    
    # Ensure that the selected_course is within the user_courses
    if selected_friend in user_friends:
        user_info.userprofile.friends.remove(selected_friend)
        #return render(request, 'delete_friend.html', {'user' : user_info, 'friend': selected_friend})
        messages.success(request, "Your friend has been deleted!")
        return HttpResponseRedirect(redirect_url)
    # Somehow selected course that was not in user list, so return an error page
    else:
        return render(request, 'error.html')

@login_required
def FriendView(request, owner=None):
    # Check if user refreshed twice: if they did then error them out eloquently
    try:
        selected_friend = User.objects.get(username=owner) 
    except:
        return render(request, 'error.html')
    user_friends = request.user.userprofile.friends.all()

    if selected_friend in user_friends:

        scheduled_courses_list = selected_friend.userprofile.scheduled_courses.all()
        comments = selected_friend.userprofile.comments_received.all()
        return render(request, 'friend_courses.html', {
            'scheduled_courses_list': scheduled_courses_list,
            'comments_received': comments,
            'friend': selected_friend
            })
    else:
        return render(request, 'error.html')

######################  Add Comments ##############################

@login_required
def AddComment(request, owner=None):
    try:
        selected_friend = User.objects.get(username=owner)
    except:
        return render(request, 'error.html')
    
    user_friends = request.user.userprofile.friends.all()
    
    if selected_friend in user_friends:
        if request.POST.get('comment'):
            msg = Comment.objects.create(comment=request.POST.get('comment'), author = request.user.username)
            selected_friend.userprofile.comments_received.add(msg)
            request.user.userprofile.comments_sent.add(msg)

            scheduled_courses_list = selected_friend.userprofile.scheduled_courses.all()
            comments = selected_friend.userprofile.comments_received.all()

    return HttpResponseRedirect('/saved-friends/'+selected_friend.username)

@login_required
def DeleteComment(request, owner=None):
    try:
        selected_friend = User.objects.get(username=owner)
    except:
        return render(request, 'error.html')

    try:
        comment = get_object_or_404(Comment, pk=request.POST['comment_choice'])
    except:
        return render(request, 'error.html')
    
    comment.delete()    

    if (request.user == selected_friend):
        return HttpResponseRedirect('/sched-courses/')
    return HttpResponseRedirect('/saved-friends/'+selected_friend.username)
        

######################  Save Courses ##############################
@login_required
def SavedCoursesView(request):
   
    saved_courses_list = request.user.userprofile.saved_courses.all()
    return render(request, 'saved_courses.html', {'saved_courses_list': saved_courses_list,})

def SaveCourse(request, slug):

    #accessing POST data sent by user (name and value variables)
    #getting specific course based on its unique ID
    try:
        course_to_save = get_object_or_404(Course, pk=request.POST['course_choice'])
    except:
        return render(request, 'error.html')

    user_saving = request.user

    #adding the course to the new UserProfile model 
    user_saving.userprofile.saved_courses.add(course_to_save)

    dictionary = {"success": True, "msg": "Course Saved Successfully" }
    #return render(request,'saved_courses.html',{'user' : user_saving, 'course' :course_to_save})
    messages.success(request, "Your course has been saved!")
    return HttpResponseRedirect(reverse('courses', args=(slug,)))

def SearchSaveCourse(request):    
    try:
        selected_course = get_object_or_404(Course, pk=request.POST['course_choice']) 
    except:
        return render(request, 'error.html')
    course_to_save = vars(selected_course)
    slug = course_to_save['dept_slug']
    # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path() #print(incoming_url)
    split_url = incoming_url.split('/')
    if split_url[1] == 'dept-list':
        redirect_url = '/dept-list/' + slug + '/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'
    else:
        redirect_url = '/saved-courses/'
    #accessing POST data sent by user (name and value variables)
    #getting specific course based on its unique ID

    user_saving = request.user

    #adding the course to the new UserProfile model 
    user_saving.userprofile.saved_courses.add(selected_course)

    dictionary = {"success": True, "msg": "Course Saved Successfully" }
    messages.success(request, "Your course has been saved!")
    return HttpResponseRedirect(redirect_url)

def DeleteCourse(request):
    # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path()
    #print(incoming_url)
    split_url = incoming_url.split('/')
    #print(split_url)
    redirect_url = ""
    if split_url[1] == 'saved-courses':
        redirect_url = '/saved-courses/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'
    
    try: 
        selected_course = get_object_or_404(Course, pk=request.POST['course_choice'])
    except:
        return render(request, 'error.html')
    
    user_courses = request.user.userprofile.saved_courses.all()
    user_info = request.user
    
    # Ensure that the selected_course is within the user_courses
    if selected_course in user_courses:
        user_info.userprofile.saved_courses.remove(selected_course)
        messages.success(request, "Your course has been deleted!")
        return HttpResponseRedirect(redirect_url)
        #return render(request, 'delete_save.html', {'user' : user_info, 'course': selected_course})
    
    # Somehow selected course that was not in user list, so return an error page
    else:
        return render(request, 'error.html')



######################  Schedule Courses ##############################
@login_required
def ScheduledCoursesView(request):
    scheduled_courses_list = request.user.userprofile.scheduled_courses.all()
    comments = request.user.userprofile.comments_received.all()
    return render(request, 'scheduled_courses.html', {
        'scheduled_courses_list': scheduled_courses_list,
        'comments_received': comments,
        })

def SaveCourseInSchedule(request, slug):
    # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path()
    #print(incoming_url)
    split_url = incoming_url.split('/')
    #print(split_url)
    redirect_url = ""
    if split_url[1] == 'dept-list':
        redirect_url = '/dept-list/' + slug + '/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'
    else:
        redirect_url = '/saved-courses/'

    
    # access course based on request ID
    try:
        selected_course = get_object_or_404(Course, pk=request.POST['course_choice']) 
    except:
        return render(request, 'error.html')
        
    course_to_save = vars(selected_course)

    # access user courses and information
    user_info = request.user
    user_courses = request.user.userprofile.scheduled_courses.all()

    # If course is asynchronous, then just add it regardless
    if len(course_to_save['start_time']) < 4:
        user_info.userprofile.scheduled_courses.add(selected_course)
        #return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})
        messages.success(request, "Your course has been scheduled!")
        return HttpResponseRedirect(redirect_url)

    start_time = int(course_to_save['start_time'][:2] + course_to_save['start_time'][3:])
    end_time = int(course_to_save['end_time'][:2] + course_to_save['end_time'][3:])
   
    day1 = course_to_save['meeting_days']
    days_of_week = [''.join(s).lower() for s in zip(day1[::2], day1[1::2])]
    print(day1)
    print(days_of_week)
    # see if there are any course conflicts
    # if any conflict: return an error page
    # else: add the course to schedule
    for saved_course in user_courses:
        dict_saved_course = vars(saved_course)
        
        
        # Check if there is no time, then just add the course regardless
        if len(dict_saved_course['start_time']) < 4:
            continue
        day2 = dict_saved_course['meeting_days']
        comp_days = [''.join(s).lower() for s in zip(day2[::2], day2[1::2])]

        diff_days = False
        for day in comp_days:
            if day in days_of_week:
               diff_days = True 

        # if not diff_days:
            # continue

        print (diff_days)
        comp_start_time = int(dict_saved_course['start_time'][:2] + dict_saved_course['start_time'][3:]) 
        comp_end_time = int(dict_saved_course['end_time'][:2] + dict_saved_course['end_time'][3:]) 
        if start_time >= comp_start_time and start_time <= comp_end_time and diff_days:
            messages.error(request, "The course " + course_to_save['dept_slug'] + " " +str(course_to_save['course_cat']) + " conflicts with " +dict_saved_course['dept_slug']+" "+ str(dict_saved_course['course_cat'])+"!")
            # return render(request, 'course_schedule_error.html', 
            #               {'user' : user_info, 
            #               'conflicted_course': saved_course,
            #               'selected_course': course_to_save})
            return HttpResponseRedirect(redirect_url)
            
        elif end_time >= comp_start_time and end_time <= comp_end_time and diff_days:
            messages.error(request, "The course " + course_to_save['dept_slug'] + " " +str(course_to_save['course_cat']) + " conflicts with " +dict_saved_course['dept_slug']+" "+ str(dict_saved_course['course_cat'])+"!")
            return HttpResponseRedirect(redirect_url)
            # return render(request, 'course_schedule_error.html', 
            #               {'user' : user_info, 
            #               'conflicted_course': saved_course,
            #               'selected_course': selected_course}) 
        elif start_time <= comp_start_time and end_time >= comp_end_time and diff_days:
            messages.error(request, "The course " + course_to_save['dept_slug'] + " " +str(course_to_save['course_cat']) + " conflicts with " +dict_saved_course['dept_slug']+" "+ str(dict_saved_course['course_cat'])+"!")
            return HttpResponseRedirect(redirect_url)
            # return render(request, 'course_schedule_error.html', 
            #               {'user' : user_info, 
            #               'conflicted_course': saved_course,
            #               'selected_course': selected_course}) 
    
    user_info.userprofile.scheduled_courses.add(selected_course)
    #return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})
    messages.success(request, "Your course has been scheduled!")
    print(request.get_full_path())
    return HttpResponseRedirect(redirect_url)
    

def SearchSaveCourseInSchedule(request):

    try:
        selected_course = get_object_or_404(Course, pk=request.POST['course_choice']) 
    except:
        return render(request, 'error.html')
    course_to_save = vars(selected_course)
    slug = course_to_save['dept_slug']
    # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path() #print(incoming_url)
    split_url = incoming_url.split('/')
    if split_url[1] == 'dept-list':
        redirect_url = '/dept-list/' + slug + '/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'
    else:
        redirect_url = '/sched-courses/'

  
    # access user courses and information
    user_info = request.user
    user_courses = request.user.userprofile.scheduled_courses.all()

    # If course is asynchronous, then just add it regardless
    if len(course_to_save['start_time']) < 4:
        user_info.userprofile.scheduled_courses.add(selected_course)
        #return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})
        messages.success(request, "Your course has been scheduled!")
        return HttpResponseRedirect(redirect_url)

    start_time = int(course_to_save['start_time'][:2] + course_to_save['start_time'][3:])
    end_time = int(course_to_save['end_time'][:2] + course_to_save['end_time'][3:])
   
    day1 = course_to_save['meeting_days']
    days_of_week = [''.join(s).lower() for s in zip(day1[::2], day1[1::2])]
    # see if there are any course conflicts
    # if any conflict: return an error page
    # else: add the course to schedule
    for saved_course in user_courses:
        dict_saved_course = vars(saved_course)
        
        
        # Check if there is no time, then just add the course regardless
        if len(dict_saved_course['start_time']) < 4:
            continue
        day2 = dict_saved_course['meeting_days']
        comp_days = [''.join(s).lower() for s in zip(day2[::2], day2[1::2])]

        diff_days = False
        for day in comp_days:
            if day in days_of_week:
               diff_days = True 

        if not diff_days:
            continue

        comp_start_time = int(dict_saved_course['start_time'][:2] + dict_saved_course['start_time'][3:]) 
        comp_end_time = int(dict_saved_course['end_time'][:2] + dict_saved_course['end_time'][3:]) 
        if start_time >= comp_start_time and start_time <= comp_end_time:
            messages.error(request, "The course " + course_to_save['dept_slug'] + " " +str(course_to_save['course_cat']) + " conflicts with " +dict_saved_course['dept_slug']+" "+ str(dict_saved_course['course_cat'])+"!")
            # return render(request, 'course_schedule_error.html', 
            #               {'user' : user_info, 
            #               'conflicted_course': saved_course,
            #               'selected_course': course_to_save})
            return HttpResponseRedirect(redirect_url)
            
        elif end_time >= comp_start_time and end_time <= comp_end_time:
            messages.error(request, "The course " + course_to_save['dept_slug'] + " " +str(course_to_save['course_cat']) + " conflicts with " +dict_saved_course['dept_slug']+" "+ str(dict_saved_course['course_cat'])+"!")
            return HttpResponseRedirect(redirect_url)
            # return render(request, 'course_schedule_error.html', 
            #               {'user' : user_info, 
            #               'conflicted_course': saved_course,
            #               'selected_course': selected_course}) 
    
    user_info.userprofile.scheduled_courses.add(selected_course)
    #return render(request, 'saved_courses.html', {'user' : user_info, 'course': selected_course})
    messages.success(request, "Your course has been scheduled!")
    print(request.get_full_path())
    return HttpResponseRedirect(redirect_url)

    
def DeleteScheduledCourse(request):
    # some logic to determine the redirect URL since this view is called from many places in the website
    incoming_url = request.get_full_path()
    #print(incoming_url)
    split_url = incoming_url.split('/')
    #print(split_url)
    redirect_url = ""
    if split_url[1] == 'sched-courses':
        redirect_url = '/sched-courses/'
    elif split_url[1] == 'profile':
        redirect_url = '/profile/'

    try: 
        selected_course = get_object_or_404(Course, pk=request.POST['course_choice'])
    except:
        return render(request, 'error.html')
    
    user_courses = request.user.userprofile.scheduled_courses.all()
    user_info = request.user
    
    # Ensure that the selected_course is within the user_courses
    if selected_course in user_courses:
        user_info.userprofile.scheduled_courses.remove(selected_course)
        #return render(request, 'delete_schedule.html', {'user' : user_info, 'course': selected_course})
        messages.success(request, "The course has been removed from your schedule!")
        return HttpResponseRedirect(redirect_url)
    # Somehow selected course that was not in user list, so return an error page
    else:
        return render(request, 'error.html')
