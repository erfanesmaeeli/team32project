from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static


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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)