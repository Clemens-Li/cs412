# Clemens Li | cl750@bu.edu | Serializers
from rest_framework import serializers
from .models import Profile, Post, Photo

class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializes a Profile into usable data '''
    class Meta:
        ''' Configuration '''
        model = Profile
        fields = ["id", "username", "display_name", "profile_image_url", "bio_text", "join_date"]

class PhotoSerializer(serializers.ModelSerializer):
    ''' Serializes a Photo into usable data '''
    class Meta:
        ''' Configuration '''
        model = Photo
        fields = ["id", "image_url", "image_file", "timestamp"]

class PostSerializer(serializers.ModelSerializer):
    ''' Serializes a Post into usable data '''
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    photos = PhotoSerializer(source="photo_set", many=True, read_only=True) # Builds each Post's Photos as a list in API (Django convention is photo_set, many=True means optionally multiple objects)
    class Meta:
        ''' Configuration '''
        model = Post
        fields = ["id", "profile", "timestamp", "caption", "photos"]

