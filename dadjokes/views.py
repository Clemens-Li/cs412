''' Clemens Li | cl750@bu.edu | Views '''
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from .models import *
from .serializers import JokeSerializer, PictureSerializer
# Create your views here.

class RandomView(TemplateView):
    ''' Displays a random Joke and Picture '''
    template_name = "dadjokes/random.html"

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data(**kwargs)
        context["joke"] = Joke.objects.order_by("?").first() # order_by("?") sorts randomly
        context["picture"] = Picture.objects.order_by("?").first() # random Picture as well
        return context

class JokeListView(ListView):
    ''' Displays all Jokes '''
    model = Joke
    template_name = "dadjokes/show_all_jokes.html"
    context_object_name = "jokes"

class JokeDetailView(DetailView):
    ''' Displays a single Joke '''
    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = "joke"

class PictureListView(ListView):
    ''' Displays all Pictures '''
    model = Picture
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = "pictures"

class PictureDetailView(DetailView):
    ''' Displays a single Picture '''
    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"

class JokeListAPIView(generics.ListCreateAPIView):
    ''' API View to return all Jokes and create '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API View to return a single Joke and read/update/delete '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListCreateAPIView):
    ''' API View to return all Pictures and create '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    ''' API View to return a single Picture and read/update/delete '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomJokeAPIView(views.APIView):
    def get(self, request):
        joke = Joke.objects.order_by("?").first()
        return Response(JokeSerializer(joke).data)

class RandomPictureAPIView(views.APIView):
    def get(self, request):
        picture = Picture.objects.order_by("?").first()
        return Response(PictureSerializer(picture).data)



    


