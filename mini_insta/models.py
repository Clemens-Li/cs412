from django.db import models

# Create your models here.
class Profile(models.Model):
    ''' The data of an Insta profile for an account'''
    # Attributes for each account's profile
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

def __str__(self):
    '''Return a string representation of this Profile object'''
    return f'{self.username}, joined {self.join_date}' # username and join_date for quick identification
