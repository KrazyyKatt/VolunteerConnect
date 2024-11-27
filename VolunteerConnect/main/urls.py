from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'main'


urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
]
