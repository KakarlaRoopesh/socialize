from django.contrib import admin
from .models import Follow, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Follow)