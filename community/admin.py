from django.contrib import admin

# Register your models here.
from .models import TubeUser, Video, Contact
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.conf import settings


admin.site.register(get_user_model(), UserAdmin)

admin.site.register(TubeUser)
admin.site.register(Video)
admin.site.register(Contact)