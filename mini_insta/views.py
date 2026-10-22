''' Clemens Li cl750@bu.edu | Views for intermediate processes '''
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin # to protect some views before login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class MiniInstaLoginRequiredMixin(LoginRequiredMixin): # had to put it up here to be used by other views
    ''' LoginRequiredMixin Subclass so that get_login_url is inherited '''
    def get_login_url(self):
        return reverse("login")

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

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data()
        # Checks if the user is authenticated and if the user's Profile follows the current Profile, then returns a boolean for redirecting context in the template
        context["is_following"] = (self.request.user.is_authenticated and Follow.objects.filter(follower_profile__user=self.request.user, profile=self.object).exists())
        return context

class PostDetailView(DetailView):
    ''' Obtains data for a single post, then directs to show_post.html '''
    model = Post
    template_name = "mini_insta/show_post.html" # HTML for a single post display
    context_object_name = "post" # singular post

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data()
        # Checks if the user is authenticated and if the user's Profile likes the current Post, then returns a boolean for redirecting context in the template
        context["is_liked"] = (self.request.user.is_authenticated and Like.objects.filter(profile__user=self.request.user, post=self.object).exists())
        return context

class CreatePostView(MiniInstaLoginRequiredMixin, CreateView): # only for users
    ''' A view to handle the creation of a Post (display HTML to user GET, process form submission and store new Post object POST)'''
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html" # HTML for the form to create a Post
    
    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data() # superclass method
        # pk = self.kwargs["pk"] # retrieve PK
        # profile = Profile.objects.get(pk=pk) # Locate correct Profile
        profile = Profile.objects.get(user=self.request.user) # Updated method of identifying Profile without PK
        context["profile"] = profile # add to context dictionary
        return context

    def form_valid(self, form):
        ''' Handles form submission, adding Profile FK to Post before submitting to database '''
        # pk = self.kwargs["pk"] # retrieve PK
        # profile = Profile.objects.get(pk=pk) # Locate correct Profile
        profile = Profile.objects.get(user=self.request.user) # Updated method of identifying Profile withou PK
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
        ''' Provide a URL to redirect to after creating a new Post '''
        pk = self.kwargs["pk"] # retrieve pk from URL pattern
        return reverse("show_post", kwargs={"pk": self.object.pk}) # call reverse to generate URL for newly created post

    # No PK, so need to define self-identification function
    def get_object(self, queryset=None):
        ''' Overrides default behavior to get the Profile of the User currently logged in '''
        return Profile.objects.get(user=self.request.user)

class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView): # only for users
    ''' A view to handle the updating of a Profile (displays UpdateProfileForm then handles the submission)'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html" # HTML for the form to update a Profile

    def form_valid(self, form):
        ''' Handles form submission for to update a Profile object '''
        print(f"UpdateProfileView: form.cleaned_data{form.cleaned_data}") # Print formatted data in terminal for visual check
        return super().form_valid(form)

    # No PK, so need to define self-identification function
    def get_object(self, queryset=None):
        ''' Overrides default behavior to get the Profile of the User currently logged in '''
        return Profile.objects.get(user=self.request.user)

class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView): # only for users
    ''' A view to handle the deletion of a Profile '''
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data() # superclass method
        context["post"] = self.object # Post to be deleted is the context object
        context["profile"] = self.object.profile # already a Post attribute
        return context

    def get_success_url(self):
        ''' Provide a URL to redirect to after deleting a Post '''
        return reverse("show_profile", kwargs={"pk": self.object.profile_id}) # reverse for dynamic URL generation

class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView): # Same as DeletePostView, only for users
    ''' A view to handle the updating of a Profile '''
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data() # superclass method
        context["post"] = self.object # Post to be deleted is the context object
        context["profile"] = self.object.profile # already a Post attribute
        return context

    def get_success_url(self):
        ''' Provide a URL to redirect to after deleting a Post '''
        return reverse("show_profile", kwargs={"pk": self.object.profile_id}) # reverse for dynamic URL generation

class ShowFollowersDetailView(DetailView):
    ''' A view to display the Followers for a single Profile object '''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    ''' A view to display the Following for a single Profile object '''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class ShowFeedView(MiniInstaLoginRequiredMixin, DetailView): # only for users
    ''' A view to display the feed for a single Profile object '''
    model = Profile
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

    # No PK, so need to define self-identification function
    def get_object(self, queryset=None):
        ''' Overrides default behavior to get the Profile of the User currently logged in '''
        return Profile.objects.get(user=self.request.user)

class SearchView(MiniInstaLoginRequiredMixin, ListView): # only for users
    ''' A view to display searches called by a single Profile object '''
    template_name = "mini_insta/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        ''' Handles requests or redirects to search.html for request submission '''
        if "query" not in self.request.GET:
            profile = self.get_object()
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        ''' Replaces model attribute in the ListView, filters Post objects containing query '''
        query = self.request.GET.get("query", "").strip() # retrieves the query from GET request
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data()
        query = self.request.GET.get("query", "").strip()
        context["profile"] = self.get_object()
        context["query"] = query
        context["posts"] = context["object_list"]

        if query:
            username_match = Profile.objects.filter(username__icontains=query) # Profiles by username
            display_name_match = Profile.objects.filter(display_name__icontains=query) # Profiles by display name
            bio_text_match = Profile.objects.filter(bio_text__icontains=query) # Profiles by bios
            context["profiles"] = (username_match | display_name_match | bio_text_match) # if a Profile's username, display name, or bio matches the query, add to context
        else:
            context["profiles"] = Profile.objects.none()

        return context

    # No PK, so need to define self-identification function
    def get_object(self, queryset=None):
        ''' Overrides default behavior to get the Profile of the User currently logged in '''
        return Profile.objects.get(user=self.request.user)

class SelfProfileDetailView(MiniInstaLoginRequiredMixin, DetailView):
    ''' For non-PK self-profile Detail View '''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    # No PK, so need to define self-identification function
    def get_object(self, queryset=None):
        ''' Overrides default behavior to get the Profile of the User currently logged in '''
        return Profile.objects.get(user=self.request.user)

class CreateProfileView(CreateView):
    ''' For the creation of a Profile '''
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        ''' Return dictionary of context variables for use in the template '''
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm(self.request.POST)
        return context

    def form_valid(self, form):
        ''' Saves the new User and its associated Profile in the database '''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        form.instance.user = user # Associates the new User with the new Profile
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend") # logs in the User right away
        return super().form_valid(form)

class FollowView(MiniInstaLoginRequiredMixin, TemplateView):
    ''' Handles the creation of a Follow relation between one Profile and another Profile '''
    def dispatch(self, request, *args, **kwargs):
        ''' Executes the creation, then redirects back to the newly followed Profile '''
        if not request.user.is_authenticated:
            return self.handle_no_permission() # If not logged in, redirect to login (I think this is coming from the mixin)
        following = Profile.objects.get(user=self.request.user) # Following
        followed = Profile.objects.get(pk=kwargs["pk"]) # Followed
        if following.pk != followed.pk: # can't follow your own Profile
            Follow.objects.get_or_create(follower_profile=following, profile=followed) # If a Follow relation already exists, just return it and don't create a duplicate
        return redirect("show_profile", pk=followed.pk) # provides PK for which Profile to display after execution

class DeleteFollowView(MiniInstaLoginRequiredMixin, TemplateView):
    ''' Handles the deletion of a Follow relation between one Profile and another Profile '''
    def dispatch(self, request, *args, **kwargs):
        ''' Executes the delete, then redirects back to the previously followed Profile'''
        if not request.user.is_authenticated:
            return self.handle_no_permission() # If not logged in, redirect to login (I think this is coming from the mixin)
        following = Profile.objects.get(user=self.request.user) # Following
        followed = Profile.objects.get(pk=kwargs["pk"]) # Followed
        Follow.objects.filter(follower_profile=following, profile=followed).delete() # Filters using the Profile parameters and deletes the relation found if it exists
        return redirect("show_profile", pk=followed.pk) # provides PK for which Profile to display after execution

class LikeView(MiniInstaLoginRequiredMixin, TemplateView):
    ''' Handles the creation of a Like relation between a Profile and a Post '''
    def dispatch(self, request, *args, **kwargs):
        ''' Executes the creation, then redirects to the newly liked Post '''
        if not request.user.is_authenticated:
            return self.handle_no_permission() # If not logged in, redirect to login
        liking = Profile.objects.get(user=self.request.user) # The Profile that is liking
        liked = Post.objects.get(pk=kwargs["pk"]) # The Post being liked
        if liking.pk != liked.pk: # can't like your own Post
            Like.objects.get_or_create(profile=liking, post=liked)
        return redirect("show_post", pk=liked.pk) # provides PK for which Post to display after execution

class DeleteLikeView(MiniInstaLoginRequiredMixin, TemplateView):
    ''' Handles the deletion of a Like relation between a Profile and a Post '''
    def dispatch(self, request, *args, **kwargs):
        ''' Executes the deletion, then redirects to the previously liked Post '''
        if not request.user.is_authenticated:
            return self.handle_no_permission() # If not logged in, redirect to login
        liking = Profile.objects.get(user=self.request.user) # The Profile that liked
        liked = Post.objects.get(pk=kwargs["pk"]) # The Post that was liked
        Like.objects.filter(profile=liking, post=liked).delete() # Filters using the Profile and Post parameters and deletes the relation found if it exists
        return redirect("show_post", pk=liked.pk) # provides PK for which Post to display after execution




