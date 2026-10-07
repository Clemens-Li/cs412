from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm

# Create your views here.

class ProfileListView(ListView):
    ''' Obtains specific data for all profiles, then directs to show_all_profiles.html '''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html" # HTML for all profiles listed
    context_object_name = "profiles" # containing many profiles

class ProfileDetailView(DetailView):
    ''' Obtains data for a single profile, then directs to show_profile.html '''
    model = Profile
    template_name = "mini_insta/show_profile.html" # HTML for a single profile page
    context_object_name = "profile" # singular profile

class PostDetailView(DetailView):
    ''' Obtains data for a single post, then directs to show_post.html'''
    model = Post
    template_name = "mini_insta/show_post.html" # HTML for a single post display
    context_object_name = "post" # singular post

class CreatePostView(CreateView):
    ''' A view to handle the creation of a Post (display HTML to user GET, process form submission and store new Post object POST)'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html" # HTML for the form to create a Post
    
    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data() # superclass method
        pk = self.kwargs["pk"] # retrieve PK
        profile = Profile.objects.get(pk=pk) # Locate correct Profile
        context["profile"] = profile # add to context dictionary
        return context

    def form_valid(self, form):
        ''' Handles form submission, adding Profile FK to Post before submitting to database '''
        pk = self.kwargs["pk"] # retrieve PK
        profile = Profile.objects.get(pk=pk) # Locate correct Profile
        form.instance.profile = profile # attach Profile to Post
        response = super().form_valid(form) # have to do this first so I can create my Photo
        files = self.request.FILES.getlist("image_file")
        for file in files: # for each file in the submission list
            Photo.objects.create( # Create a Photo after saving Post
                post=self.object,
                image_file = file
                # image_url=self.request.POST['image_url'] not needed anymore
            )
        return response

    def get_success_url(self):
        ''' Provide a URL to redirect after creating a new Post '''
        pk = self.kwargs["pk"] # retrieve pk from URL pattern
        return reverse("show_post", kwargs={"pk": self.object.pk}) # call reverse to generate URL for newly created post

    
