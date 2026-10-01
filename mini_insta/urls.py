# URLs for Mini_Insta App
from django.urls import path
from django.conf import settings
from .views import ProfileDetailView, ProfileListView
urlpatterns = [
    path(r"", ProfileListView.as_view(), name="show_all_profiles"), # empty path just leads to main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
]