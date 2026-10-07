from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from .models import Profile, Post
from .forms import CreatePostForm

# Create your views here.

class ProfileListView(ListView):
    ''' Obtains specific data for all profiles, then directs to show_all_profiles.html '''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html" # HTML for all profiles listed
    context_object_name = "profiles" # containing many profiles

class ProfileDetailView(DetailView):
    ''' Obtains data for a single profile, then directs to show_profile.html '''
    model = Profile
    template_name = "mini_insta/show_profile.html" # HTML for a single profile page
    context_object_name = "profile" # singular profile

class PostDetailView(DetailView):
    ''' Obtains data for a single post, then directs to show_post.html'''
    model = Post
    template_name = "mini_insta/show_post.html" # HTML for a single post display
    context_object_name = "post" # singular post

class CreatePostView(CreateView):
    ''' A view to handle the creation of a Post (display HTML to user GET, process form submission and store new Post object POST)'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html" # HTML for the form to create a Post