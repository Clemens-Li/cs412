from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile
# Create your views here.

class ProfileListView(ListView):
    ''' Obtains data for all profiles, then directs to show_all_profiles.html '''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html" # HTML for all profiles
    context_object_name = "profiles" # containing many profiles
