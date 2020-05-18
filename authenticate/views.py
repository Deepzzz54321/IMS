from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import credentials
from institute.models import Employees
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from inventorydb.settings import EMAIL_HOST_USER


# Create your views here.
def login(request):

    if request.COOKIES.get('username'):
        response = render(request, 'authenticate/login.html')
        response.delete_cookie('username')
        return response    
    
    if request.method == 'POST':
        user = request.POST["username"]
        password1 = request.POST["password"]
        if credentials.objects.filter(emp_id=user, password=password1).exists():
            response = redirect('institute:official_home')
            response.set_cookie('username',user)
            return response       

        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('authenticate:login')

    return render(request, 'authenticate/login.html')

@csrf_exempt
def signup(request):

    if request.COOKIES.get('username'):
        response = render(request, 'authenticate/SignUp1.html')
        response.delete_cookie('username')
        return response  
    
    if request.method == 'POST':
        regno = request.POST["regno"]
        password1 = request.POST["pass"]

        if credentials.objects.filter(emp_id=regno).exists():
            messages.error(request, 'Official already exists. Please Login!')
            return redirect('authenticate:signup')
        
        else:
            if Employees.objects.filter(emp_id = regno).exists():
                newCred = credentials(emp_id= Employees.objects.get(emp_id = regno), password=password1)
                newCred.save()
                messages.success(request, 'User added successfully!')
                return redirect('authenticate:signup')
            else:
                messages.error(request, 'No Official with given Registration no.')
                return redirect('authenticate:signup')                  
    
    return render(request, 'authenticate/SignUp1.html')



def forgot(request):
    if request.method == 'POST':
        user = request.POST["username"]
        if credentials.objects.filter(emp_id=user).exists():
            newPass = credentials.objects.get(emp_id_id=str(user))
            use=Employees.objects.get(emp_id=user)
            email=use.email_id
            subject="NIT AP Inventory Management System-Forgot Password request!"
            message="The password for the username \n"+str(user)+" is "+"\n Password : "+str(newPass.password)+"\nThis is a computer generated message dont reply to this !This is from Hostel Management System NIT AP .If it is not you please report to admin of the website "
            recepient=str(email)
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            messages.success(request, 'Password is sent to your mail id!')
            return redirect('authenticate:login')

        else:
            messages.error(request, 'Invalid Username')
            return redirect('authenticate:forgot')    

    return render(request, 'authenticate/forgot.html')