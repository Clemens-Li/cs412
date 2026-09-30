from django.shortcuts import render
from django.view.generic import ListView
from .models import Profile
# Create your views here.

class ProfileListView(ListView):
    ''' Obtains data for all profiles, then directs to show_all_profiles.html '''

