from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO  # Updated model name
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def home(request):
    return render(request, 'sign.html')

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm, emailid, pwd)
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/login')
    
    return render(request, 'sign.html')

def login_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)
        user = authenticate(request, username=fnm, password=pwd)  # Fixed 'Username' to 'username'
        if user is not None:
            auth_login(request, user)  # Use 'auth_login' to avoid conflict with the view function name
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request, 'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO(title=title, user=request.user)  # Use 'Todo' (singular class name)
        obj.save()
        res = models.TODO.objects.filter(user=request.user).order_by('-date')  # 'Todo' singular
        return redirect('/todopage')  # Remove context from redirect
    res = models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        
        return redirect('/todopage')  # Redirect without passing context
    obj = models.TODO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})  # Pass context to render

@login_required(login_url='/login')
def delete_todo(request, srno):
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')
