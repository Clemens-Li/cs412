''' Clemens Li cl750@bu.edu | Contains forms used for CRUD operations on Posts and Profiles '''
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    ''' A form to add a Post to the database '''
    class Meta:
        ''' Specifies that this form is associated with a model from our database'''
        model = Post
        fields = ["caption"] # having timestamp isn't editable, and having profile is messy

class UpdateProfileForm(forms.ModelForm):
    ''' A form to update an existing Profile in the database '''
    class Meta:
        ''' Specifies that this form is associated with a model from our database '''
        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"] # Modifiable fields; can't change username or join_date

class UpdatePostForm(forms.ModelForm): # Exact same as CreatePostForm, just different name for clarity
    ''' A form to update an existing Post in the database '''
    class Meta:
        ''' Specifies that this form is associated with a model from our database '''
        model = Post
        fields = ["caption"] # Modifiable fields; can't change username or join_date

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile '''
    class Meta:
        ''' Specifies that this form is associated with a model from our database '''
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]