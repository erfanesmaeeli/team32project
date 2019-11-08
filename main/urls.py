from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('contact/', views.contact),
    path('login/', views.login_),
    path('logout/', views.logout_),
    path('profile/', views.profile),
    path('profile-edit/', views.profile_edit),
    path('panel/', views.panel),
    path('new-course/', views.new_course),
    path('courses/', views.courses),
]