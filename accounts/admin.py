from django.contrib import admin
from .models import Profile 
from django.contrib.auth.admin import UserAdmin
from  django.contrib.auth.models import User
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
     list_display=['user','location','bio']