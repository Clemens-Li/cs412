from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r"main", views.main_page, name="main"),
    path(r"order", views.order_page, name="order"),
    path(r"confirmation", views.confirmation_page, name="confirmation")
]