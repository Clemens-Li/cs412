# Clemens Li | cl750@bu.edu | Serializers
from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ["text", "name", "timestamp"]

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ["image_url", "name", "timestamp"]