from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

#user: admin
#pass: admin1234

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_superuser']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)



admin.site.register([CustomUser, Event, Comment, Participation, Attachment])