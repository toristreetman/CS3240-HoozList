from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Welcome to the better Lou's List!")

def login(request):
    return render(request, 'app.html', {})
