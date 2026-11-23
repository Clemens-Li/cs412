from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post, Profile


class TokenAuthTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("post-owner", password="test-password")
        self.owner_profile = Profile.objects.create(user=self.owner)
        self.other = User.objects.create_user("another-user", password="test-password")
        self.post = Post.objects.create(
            profile=self.owner_profile,
            caption="Original caption",
        )

    def authenticate_user(self, username, password="test-password"):
        response = self.client.post(
            reverse("api_login"),
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}",
        )

    def test_registration_creates_user_and_profile(self):
        response = self.client.post(
            reverse("api_register"),
            {"username": "new-user", "password": "new-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        user = User.objects.get(username="new-user")
        self.assertTrue(user.check_password("new-password"))
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_login_returns_token_and_profile_id(self):
        response = self.client.post(
            reverse("api_login"),
            {"username": self.owner.username, "password": "test-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["token"])
        self.assertEqual(response.data["profile_id"], self.owner_profile.id)

    def test_login_uses_first_profile_when_user_has_multiple(self):
        Profile.objects.create(user=self.owner, username="second-profile")

        response = self.client.post(
            reverse("api_login"),
            {"username": self.owner.username, "password": "test-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_id"], self.owner_profile.id)

    def test_bad_login_is_rejected(self):
        response = self.client.post(
            reverse("api_login"),
            {"username": self.owner.username, "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_create_requires_owner(self):
        url = reverse("profile_posts_api", args=[self.owner_profile.id])
        payload = {"caption": "New caption"}

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authenticate_user(self.other.username)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.owner.username)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["profile"], self.owner_profile.id)

    def test_post_update_requires_owner(self):
        url = reverse("post_update_api", args=[self.post.id])
        payload = {"caption": "Updated caption"}

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authenticate_user(self.other.username)
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.owner.username)
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption"], "Updated caption")

    def test_post_delete_requires_owner(self):
        url = reverse("post_delete_api", args=[self.post.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authenticate_user(self.other.username)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.authenticate_user(self.owner.username)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.id).exists())
