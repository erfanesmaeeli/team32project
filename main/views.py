from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password_repeat = request.POST.get("password2")
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)
        user.save()

        return HttpResponseRedirect("/")
    return render(request, "signup.html")


def contact(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        return render(request, "contact-done.html")
    return render(request, "contact.html")


def login_(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        elif user is None:
            error = True
    return render(request, "login.html", {
        "error": error
    })


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")
    return render(request, "login.html")