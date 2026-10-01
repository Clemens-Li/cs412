from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile) # so that I can perform CRUD ops and add sample users