from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, ("There Was An Error Logging In, Try Again."))
            return redirect('login')
        
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully."))
    return redirect('home')



