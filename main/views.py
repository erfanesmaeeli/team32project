from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def signup(request):
    error_pass = False
    error_user = False
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password_repeat = request.POST.get("password2")
        if password != password_repeat :
            error_pass = True
            return render(request, "signup.html", {"error_pass": error_pass})

        if User.objects.filter(username=username).exists() :
            error_user = True
            return render(request, "signup.html", {"error_user": error_user})

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)
        user.save()

        return HttpResponseRedirect("/")
    return render(request, "signup.html")


def contact(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        text = request.POST.get("text")
        email = request.POST.get("email")
        my_email = EmailMessage(
                title,
                f"{text}  {email}",
                'ES Band Webelopers' + '<webelopers.esband@gmail.com>',
                ["webe19lopers@gmail.com"],
            )
        my_email.send()
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


def profile(request):
    return render(request, "profile.html")


def profile_edit(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if first_name != "":
            request.user.first_name = first_name
        if last_name != "":
            request.user.last_name = last_name
        return render(request, "profile.html")
    return render(request, "profile-edit.html")


def panel(request):
    return render(request, "panel.html")


def new_course(request):
    return render(request, "new-course.html")


def courses(request):
    return render(request, "courses.html")