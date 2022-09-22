import imp
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Item
from django.contrib.auth.models import User
from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from allauth.account.models import EmailAddress
from rest_framework.views import APIView


class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
        username="testuser",
        email="test@email.com",
        password="secret",
        )

        cls.item = Item.objects.create(
        title= "Item 6",
        price= 60,
        slug="item-6",
        )

    def test_api_ItemListview(self):
        response = self.client.get(reverse("api-home"))
        self.assertEqual(self.item.title, "Item 6")
        self.assertEqual(self.item.slug, "item-6")


    def test_api_detailview(self): 
        response = self.client.get(
        reverse("api-detail", kwargs={"slug": self.item.slug}),
        format="json"
        )
        self.assertEqual(self.item.title, "Item 6")
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(self.item.slug, "item-6")

    def test_username_containing_at(self):
        user = get_user_model().objects.create(username="@raymond.penners")
        user.set_password("psst")
        user.save()
        EmailAddress.objects.create(
            user=user,
            email="raymond.penners@example.com",
            primary=True,
            verified=True,
        )
        my_response = self.client.post(
            reverse("account_login"),
            {"login": "@raymond.penners", "password": "psst"},
        )
        self.assertRedirects(
            my_response, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False
        )

    

    
    def _create_user(self, username="user1", password="password", **kwargs):
        user = get_user_model().objects.create(
            username=username, is_active=True, **kwargs
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def _create_user_and_login(self, usable_password=True):
        password = "doe" if usable_password else False
        user = self._create_user(password=password)
        self.client.force_login(user)
        return user

    def test_set_password_not_allowed(self):
        user = self._create_user_and_login(True)
        pwd = "!*312uwni112"
        self.assertFalse(user.check_password(pwd))
        resp = self.client.post(
            reverse("account_set_password"),
            data={"password1": pwd, "password2": pwd},
        )
        user.refresh_from_db()
        self.assertFalse(user.check_password(pwd))
        self.assertTrue(user.has_usable_password())
        self.assertEqual(resp.status_code, 302)

    