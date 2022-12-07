from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('dept-list/', views.DepartmentView, name='department_view'),
    path('dept-list/<slug:slug>/', views.CoursesView.as_view(), name='courses'),
    path('dept-list/<slug:slug>/save_course', views.SaveCourse, name='save_course'),
    path('dept-list/<slug:slug>/save_schedule', views.SaveCourseInSchedule, name = 'save_schedule'),
    
    path('profile/', views.ProfileView, name='profile_view'),
    path('profile/<slug:slug>/save_schedule2', views.SaveCourseInSchedule, name = 'save_schedule2'),
    path('profile/delete_save', views.DeleteCourse, name = 'delete_save'),
    path('profile/delete_schedule', views.DeleteScheduledCourse, name='delete_schedule'),
    path('profile/save_friend', views.SaveFriend, name='save_friend'),
    path('profile/delete_friend', views.DeleteFriend, name='delete_friend'),
    path('profile/search_friend', views.SearchFriendView, name='search_friend'),
    
    path('saved-courses/', views.SavedCoursesView, name='saved_courses_view'),
    path('saved-courses/delete_save', views.DeleteCourse, name = 'delete_save2'),
    path('saved-courses/<slug:slug>/save_schedule3', views.SaveCourseInSchedule, name = 'save_schedule3'),
    
    path('sched-courses/', views.ScheduledCoursesView, name='sched_courses_view'),
    path('sched-courses/delete_schedule',  views.DeleteScheduledCourse, name='delete_schedule2'),
   
    path('saved-friends/', views.SavedFriendsView, name='saved_friends_view'),
    path('saved-friends/delete_friend', views.DeleteFriend, name='delete_friend2'),
    path('saved-friends/<str:owner>', views.FriendView, name='friend_view'),
    path('saved-friends/<str:owner>/add_comment', views.AddComment, name='add_comment'),
    path('saved-friends/<str:owner>/del_comment', views.DeleteComment, name='del_comment'),

    path('search_view/', views.SearchView, name='search_view'),
    path('search_view/save_course', views.SearchSaveCourse, name='search_save_course'),
    path('search_view/save_schedule', views.SearchSaveCourseInSchedule, name = 'search_save_schedule'),
    path('user-settings', views.userSettings, name='user-settings'),
    path('user-settings-update', views.userSettingsUpdate, name='user-settings-update'),
    
]
    
    
    
