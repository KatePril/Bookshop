from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class Users2(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'image_thumbnail')