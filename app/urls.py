from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('dept-list/', views.DepartmentView, name='department_view'),
    path('dept-list/<slug:slug>/', views.CoursesView.as_view(), name='courses'),
    path('profile/', views.ProfileView, name='profile_view'),
    
]
    
    
    