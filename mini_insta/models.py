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

    def get_all_posts(self):
        ''' Returns all Post objects with the caller Profile object as the foreign key '''
        return Post.objects.filter(profile=self).order_by("timestamp") # Filters all Post-class object with itself as the foreign key and orders by oldest first

# Secondary Model for posts in each profile
class Post(models.Model):
    ''' The metadata of an Instagram post found in a profile '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # Foreign key profile, if parent profile deleted child posts are deleted
    timestamp = models.DateTimeField(auto_now=True) # Time Posted
    caption = models.TextField(blank=True) # optional caption

    def __str__(self):
        ''' Return a string representation of this Post object '''
        return f'Posted by {self.profile.username} at {self.timestamp}' # username and post time

    def get_all_photos(self):
            ''' Returns all Photo objects with the caller Post object as the foreign key '''
            return Photo.objects.filter(post=self).order_by("timestamp") # Filters all Photo-class object with itself as the foreign key and orders by oldest first

class Photo(models.Model):
    ''' The metadata of a single photo used in a Post object'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Foreign key post, if a post is deleted all of the photos in that post are also deleted
    image_url = models.TextField(blank=True) # for the actual photo
    timestamp = models.DateTimeField(auto_now=True) # Time Photo was created/saved

    def __str__(self):
        ''' Return a string representation of this Photo object '''
        return f'Photo posted by {self.post.profile.username}, saved at {self.timestamp}' # Username and time saved