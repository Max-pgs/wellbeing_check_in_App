from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthAccessTests(TestCase):
    def test_checkins_requires_login(self):
        resp = self.client.get("/checkins/", follow=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_user_can_login(self):
        User.objects.create_user(username="testuser", password="pass12345")
        logged_in = self.client.login(username="testuser", password="pass12345")
        self.assertTrue(logged_in)