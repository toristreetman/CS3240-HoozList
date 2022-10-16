from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('<slug:slug>/', views.DepartmentView.as_view(), name='department')
]
    
    
    