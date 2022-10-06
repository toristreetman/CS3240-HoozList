from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
#@csrf_exempt
def index(request):
    return HttpResponse("Welcome to the better Lou's List!")
#@csrf_exempt
def login(request):
    return render(request, 'app.html', {})
