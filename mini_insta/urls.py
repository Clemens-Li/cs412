# mini_insta/urls.py
# URLs for Mini_Insta App
from django.urls import path
from django.conf import settings
from .views import * # ProfileListView, ProfileDetailView, PostDetailView
urlpatterns = [
    path(r"", ProfileListView.as_view(), name="show_all_profiles"), # empty path just leads to main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"), # per profile, with pk as primary key for the Profile
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"), # Create a post
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post") # per post, with pk as primary key for the Post
]