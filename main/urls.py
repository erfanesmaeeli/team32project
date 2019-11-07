from django.contrib import admin
from django.urls import path, include
from main import views


urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('contact/', views.contact),
    path('login/', views.login_),
]