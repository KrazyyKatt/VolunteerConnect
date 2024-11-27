from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'main'  # here for namespacing of urls.


urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),  # Home stranica na root URL-u
    path('register/', views.register, name='register'),
]
