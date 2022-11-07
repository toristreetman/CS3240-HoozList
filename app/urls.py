from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('dept-list/', views.DepartmentView, name='department_view'),
    path('dept-list/<slug:slug>/', views.CoursesView.as_view(), name='courses'),
    path('profile/', views.ProfileView, name='profile_view'),
    path('search_view/', views.SearchView, name='search_view'),
    path('dept-list/<slug:slug>/save_course', views.SaveCourse, name='save_course'),
    path('dept-list/<slug:slug>/save_schedule', views.SaveCourseInSchedule, name = 'save_schedule'),
    path('profile/<slug:slug>/save_schedule2', views.SaveCourseInSchedule, name = 'save_schedule2'),
    path('profile/delete_save', views.DeleteCourse, name = 'delete_save'),
    path('profile/delete_schedule', views.DeleteScheduledCourse, name='delete_schedule')
]
    
    
    