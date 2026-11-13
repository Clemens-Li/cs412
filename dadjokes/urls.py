''' Clemens Li cl750@bu.edu | URL Patterns '''
# URLs for Dadjokes App
from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path(r"", RandomView.as_view(), name=""),
    path(r"random", RandomView.as_view(), name="random"),
    path(r"jokes", JokeListView.as_view(), name="jokes"),
    path(r"joke/<int:pk>", JokeDetailView.as_view(), name="joke"),
    path(r"pictures", PictureListView.as_view(), name="pictures"),
    path(r"picture/<int:pk>", PictureDetailView.as_view(), name="picture"),
    path(r"api/", RandomJokeAPIView.as_view()),
    path(r"api/random", RandomJokeAPIView.as_view()),
    path(r"api/jokes", JokeListAPIView.as_view()),
    path(r"api/joke/<int:pk>", JokeDetailAPIView.as_view()),
    path(r"api/pictures", PictureListAPIView.as_view()),
    path(r"api/picture/<int:pk>", PictureDetailAPIView.as_view()),
    path(r"api/random_picture", RandomPictureAPIView.as_view())
]
