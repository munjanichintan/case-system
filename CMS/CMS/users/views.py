from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as dj_login
from myapp.views import *
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    return render(request, 'users/index.html')


def signup(request):
    if request.method == "POST":
        # person_id = Person.objects.latest('person_id')
        user_type = request.POST['user_type'] 
        username = request.POST['username']
        password = make_password(request.POST['password'])
        print(password)
        # con_password = make_password(request.POST['con-password'])
        # print(con_password)
        creation_date = request.POST.get('creation_date')
        changed_date = request.POST.get('changed_date')
        data = User.objects.filter(username=username).exists()
        print(data)
        if data:
            msg = "Username Already Exists"
            return render(request, 'users/register.html',{'msg':msg})
        user = User(user_type=user_type,username=username,password=password,creation_date=creation_date,changed_date=changed_date)
        user.save()
        return redirect('signin')
    return render(request, 'users/register.html')


def signin(request):
    if request.method == 'POST':
        password = make_password(request.POST['password'])
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            dj_login(request, user)
            return redirect('casedetailpage')  
        else:
            messages.error(request, "Username and Password is wrong !")
            return redirect('signin')
    return render(request, 'users/login.html') 
