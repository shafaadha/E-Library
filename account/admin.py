from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import ProfileModel

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ProfileModel)

