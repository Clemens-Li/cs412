''' Clemens Li cl750@bu.edu | Registration of created models '''
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile) # so that I can perform CRUD ops and add sample users
admin.site.register(Post) # for manually adding posts
admin.site.register(Photo) # and photos
admin.site.register(Follow) # and follows
admin.site.register(Comment) # and comments
admin.site.register(Like) # and likes