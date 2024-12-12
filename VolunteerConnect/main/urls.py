from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import view_event

app_name = 'main'


urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    #Provjere
    path('event/', view_event, name='view_event'),

]
