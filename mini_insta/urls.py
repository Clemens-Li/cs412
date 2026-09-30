# URLs for Mini_Insta App
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r"", views.ProfileListView, name="show_all_profiles"), # empty path just leads to main
]