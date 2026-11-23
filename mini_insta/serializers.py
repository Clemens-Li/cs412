# Clemens Li | cl750@bu.edu | Serializers
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Post, Photo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializes a Profile into usable data '''
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        ''' Configuration '''
        model = Profile
        fields = [
            "id", "username", "display_name", "profile_image_url", "bio_text",
            "join_date", "follower_count", "following_count",
        ]

    def get_follower_count(self, profile):
        return profile.get_num_followers()

    def get_following_count(self, profile):
        return profile.get_num_following()

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

