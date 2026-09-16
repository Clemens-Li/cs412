from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r"", views.quote_page, name="main"),
    path(r"quote", views.quote_page, name="quote"),
    path(r"show_all", views.show_all_page, name="show_all"),
    path(r"about", views.about_page, name="about")
]