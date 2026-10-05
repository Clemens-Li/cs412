from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo
admin.site.register(Profile) # so that I can perform CRUD ops and add sample users
admin.site.register(Post) # for manually adding posts
admin.site.register(Photo) # and photos