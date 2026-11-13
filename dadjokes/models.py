''' Clemens Li | cl750@bu.edu | Data Models '''
from django.db import models

# Create your models here.
class Joke(models.Model):
    ''' The data for a Joke object '''
    text = models.TextField() # The text of the Joke
    name = models.TextField() # The name of the Joke's contributor
    timestamp = models.DateTimeField(auto_now=True) # The timestamp of when the Joke was created

class Picture(models.Model):
    ''' The data for a Picture object '''
    image_url = models.TextField() # The URL of the image
    name = models.TextField() # The name of the Picture's contributor
    timestamp = models.DateTimeField(auto_now=True) # The timestamp of when the Picture was created

