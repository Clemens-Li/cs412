''' Clemens Li cl750@bu.edu | Model designs (Photo, Post, Profile)'''
from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        ''' Returns the absolute URL of the profile for reference using reverse'''
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_followers(self):
        ''' Returns a list of all Profiles following this Profile object'''
        followers = Follow.objects.filter(profile=self) # finds all Follow relations containing itself as the followed Profile FK
        return [follow.follower_profile for follow in followers] # makes a list containing a Profile for each relation

    def get_num_followers(self):
        ''' Returns the number of Profiles following this Profile object '''
        return Follow.objects.filter(profile=self).count() # counts the Follow relations containing itself as the followed Profile FK

    def get_following(self):
        ''' Returns a list of all Profiles followed by this Profile object '''
        following = Follow.objects.filter(follower_profile = self) # finds all Follow relations containing itself as the following Profile FK
        return [follow.profile for follow in following] # makes a list containing a Profile for each relation

    def get_num_following(self):
        ''' Returns the number of Profiles followed by this Profile object '''
        return Follow.objects.filter(follower_profile=self).count()
    
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
        return Photo.objects.filter(post=self).order_by("timestamp") # Filters all Photo objects with itself as the foreign key and orders by oldest first

    def get_all_comments(self):
        ''' Returns all Comment objects with the caller Post object as the foreign key '''
        return Comment.objects.filter(post=self) # Filters all Comment objects with itself as the foreign key

    def get_likes(self):
        ''' Returns all Like objects with the caller Post object as the foreign key '''
        return Like.objects.filter(post=self) # Filters all Like objects with itself as the foreign key
    
class Photo(models.Model):
    ''' The metadata of a single photo used in a Post object'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Foreign key post, if a post is deleted all of the photos in that post are also deleted
    image_url = models.TextField(blank=True) # for the photo URL
    timestamp = models.DateTimeField(auto_now=True) # Time Photo was created/saved
    image_file = models.ImageField(blank=True) # for photo file

    def __str__(self):
        ''' Return a string representation of this Photo object '''
        return f'Photo posted by {self.post.profile.username}, saved at {self.timestamp}; URL: {self.get_image_url()}' # Username and time saved

    def get_image_url(self):
        ''' Either return image_url attribute, else the url of the image_file attribute'''
        if (self.image_url):
            return self.image_url
        else:
            return self.image_file.url

class Follow(models.Model):
    ''' The metadata of a relation associating 2 Profiles with each other '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile") # the profile being followed
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile") # the profile doing the following
    timestamp = models.DateTimeField(auto_now=True) # Timestamp for when follower_profile followed profile

    def __str__(self):
        followed = self.profile.display_name or self.profile.username # if display_name doesn't exist, show username
        follower = self.follower_profile.display_name or self.follower_profile.username # if display_name doesn't exist, show username
        return f"{follower} follows {followed}"

class Comment(models.Model):
    ''' The metadata of a Comment relation associating a Profile and a Post with each other '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Associated Post FK
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # Associated Profile FK
    timestamp = models.DateTimeField(auto_now=True) # time commented
    text = models.TextField(blank=True) # comment text

    def __str__(self):
        return f"{self.profile.username} commented on Post #{self.post_id} at {self.timestamp}"
    
class Like(models.Model):
    ''' The metadata of a Like relation associating a Profile and a Post with each other '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # Associated Post FK
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # Associated Profile FK
    timestamp = models.DateTimeField(auto_now=True) # time commented

    def __str__(self):
        return f"{self.profile.username} liked Post #{self.post_id} at {self.timestamp}"
