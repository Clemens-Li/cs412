''' Clemens Li cl750@bu.edu | URL Patterns for profile and post views'''
# mini_insta/urls.py
# URLs for Mini_Insta App
from django.urls import path
from django.conf import settings
from .views import * # ProfileListView, ProfileDetailView, PostDetailView
urlpatterns = [
    path(r"", ProfileListView.as_view(), name="show_all_profiles"), # empty path just leads to main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"), # per profile, with pk as primary key for the Profile
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"), # Create a post
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"), # per post, with pk as primary key for the Post
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"), # per profile, with pk as primary key for the Profile
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"), # per post, with pk as primary key for the Post
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"), # per post, with pk as primary key for the Post
    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"), # per profile, with pk as primary key for the Profile
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"), # per profile, with pk as primary key for the Profile
    path("profile/<int:pk>/feed", ShowFeedView.as_view(), name="show_feed") # per profile, with pk as primary key for the Profile
]