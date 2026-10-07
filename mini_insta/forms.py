from django import forms
from models import *

class CreatePostForm(forms.modelForm):
    ''' A form to add a Post to the database '''
    class Meta:
        ''' Specifies that this form is associated with a model from our database'''
        model = Post
        fields = ["caption, timestamp"]