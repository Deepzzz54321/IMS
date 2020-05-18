from django.shortcuts import render
from django.http import HttpResponse
from institute.models import Employees

# Create your views here.
def official_home(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    return HttpResponse('<h1>'+user+'</h1>')