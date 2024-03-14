from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from . forms import CreateUserFrom


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request,("you did something wrong try again")) 
            return redirect("login")
        
    else:
        return render(request, "auth/login.html" ,{})


def logout_user(request):
    logout(request)
    messages.success(request,("you are logged out")) 
    return redirect("home")


def create_user(request):
    if request.method == 'POST':
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("sign up successful"))
            return redirect("home")

    else:
        form = CreateUserFrom()

    return render(request, "auth/create_user.html", {"form":form})