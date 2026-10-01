from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Profile
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