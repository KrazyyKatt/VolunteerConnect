"""
URL configuration for VolunteerConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect

def redirect_to_home(request):
    return redirect('main:home')  # Namespace 'main' i ruta 'home'


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', redirect_to_home, name='redirect_to_home'),  # Root URL preusmjerava na 'main:home'
    path('', include('main.urls')),  # Inkluzija svih ruta iz aplikacije 'main'
    path('admin/', admin.site.urls),
]
