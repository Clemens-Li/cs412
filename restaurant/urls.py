# URLs for restaurant app
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r"", views.main_page, name=""), # empty path just leads to main
    path(r"main", views.main_page, name="main"),
    path(r"order", views.order_page, name="order"), # ordering page
    path(r"confirmation", views.confirmation_page, name="confirmation") # confirmation page
]