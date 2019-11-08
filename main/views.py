from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from main.models import Course, UserCourse
import time
from datetime import datetime


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


def profile(request):
    return render(request, "profile.html")


def profile_edit(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        image = request.FILES.get("profile_image")

        if first_name != "":
            request.user.first_name = first_name
            request.user.save()
        if last_name != "":
            request.user.last_name = last_name
            request.user.save()
        if image:
            request.user.profile.image = image
            request.user.save()
        return render(request, "profile.html")
    return render(request, "profile-edit.html")


def panel(request):
    return render(request, "panel.html")


def new_course(request):
    if request.method == "POST":
        error_time = False
        department = request.POST.get("department")
        name = request.POST.get("name")
        course_number = request.POST.get("course_number")
        group_number = request.POST.get("group_number")
        teacher = request.POST.get("teacher")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        first_day = request.POST.get("first_day")
        second_day = request.POST.get("second_day")
        exam_date = request.POST.get("exam_date")

        try:
            time.strptime(start_time, '%H:%M')
        except ValueError:
            error_time = True
            return render(request, "new-course.html", {"error_time": error_time})

        try:
            time.strptime(end_time, '%H:%M')
        except ValueError:
            error_time = True
            return render(request, "new-course.html", {"error_time": error_time})
        try:
            datetime.strptime(exam_date, '%Y-%m-%d')
        except ValueError:
            error_time = True
            return render(request, "new-course.html", {"error_time": error_time})

        course = Course(department=department, name=name, course_number=course_number, group_number=group_number,
                        teacher=teacher, start_time=start_time, end_time=end_time, exam_date=exam_date,
                        first_day=first_day, second_day=second_day)
        course.save()
        return render(request, "panel.html")

    return render(request, "new-course.html")


def courses(request):
    user_course = [c.course for c in UserCourse.objects.all()]
    courses = Course.objects.all()
    if request.method == "POST":
        query = request.POST.get("search_query")
        s1 = request.POST.get("department")
        s2 = request.POST.get("teacher")
        s3 = request.POST.get("course")
        print(s1,s2,s3)
        if query:
            if s1 is not None:
                search_list = Course.objects.filter(Q(department__icontains=query))
            elif s2 is not None:
                search_list = Course.objects.filter(Q(teacher__icontains=query))
            elif s3 is not None:
                search_list = Course.objects.filter(Q(name__icontains=query))
            else:
                search_list = Course.objects.filter(Q(department__icontains=query))
            return render(request, "courses.html", {"search_list": search_list })
    return render(request, "courses.html" , {"courses": courses , "user_course": user_course})


def add(request, pk):
    request.user.usercourse_set.create(course__id=pk)