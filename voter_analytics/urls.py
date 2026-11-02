''' Clemens Li | cl750@bu.edu | URL Patterns '''
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("", VoterListView.as_view(), name="voters"), # View all Voters
    path("voter/<int:pk>", VoterDetailView.as_view(), name="voter"), # View a Voter
    path("graphs", GraphListView.as_view(), name="graphs") # View all graphs
]