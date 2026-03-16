from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .models import CheckIn


class AuthAccessTests(TestCase):
    def test_checkins_requires_login(self):
        resp = self.client.get("/checkins/", follow=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_user_can_login(self):
        User.objects.create_user(username="testuser", password="pass12345")
        logged_in = self.client.login(username="testuser", password="pass12345")
        self.assertTrue(logged_in)


class ApiTests(TestCase):
    def setUp(self):
        # two users
        self.user1 = User.objects.create_user(username="u1", password="pass12345")
        self.user2 = User.objects.create_user(username="u2", password="pass12345")

        # create checkins for both users
        self.c1 = CheckIn.objects.create(
            user=self.user1,
            checkin_date=date(2026, 3, 1),
            energy_score=3,
            mood_score=2,
            activity_score=4,
        )
        self.c2 = CheckIn.objects.create(
            user=self.user2,
            checkin_date=date(2026, 3, 2),
            energy_score=5,
            mood_score=5,
            activity_score=5,
        )

    def test_api_checkins_requires_login(self):
        resp = self.client.get("/checkins/api/checkins/")
        self.assertEqual(resp.status_code, 302)  # should redirect to login

    def test_api_checkins_returns_user_scoped_data(self):
        # login as user1
        self.client.login(username="u1", password="pass12345")

        resp = self.client.get("/checkins/api/checkins/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("items", data)

        # should only contain user1's checkin(s)
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["checkin_date"], "2026-03-01")

    def test_progress_api_returns_expected_shape(self):
        self.client.login(username="u1", password="pass12345")

        resp = self.client.get("/checkins/api/progress/?from=2026-03-01&to=2026-03-03")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertIn("from", data)
        self.assertIn("to", data)
        self.assertIn("summary", data)
        self.assertIn("trends", data)
        self.assertIn("achievements", data)

        self.assertIn("avg_energy", data["summary"])
        self.assertIn("avg_mood", data["summary"])
        self.assertIn("avg_activity", data["summary"])
        self.assertIn("total_checkins", data["summary"])

    def test_progress_invalid_date_returns_400(self):
        resp = self.client.get("/checkins/api/progress/?from=not-a-date")
        self.assertEqual(resp.status_code, 400)
            

class OwnershipTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass12345")
        self.other = User.objects.create_user(username="other", password="pass12345")

        self.checkin = CheckIn.objects.create(
            user=self.owner,
            checkin_date=date(2026, 3, 1),
            energy_score=3,
            mood_score=2,
            activity_score=4,
        )

    def test_other_user_cannot_edit_someone_elses_checkin(self):
        self.client.login(username="other", password="pass12345")
        resp = self.client.get(f"/checkins/{self.checkin.pk}/edit/")
       
        self.assertIn(resp.status_code, (403, 404))

    def test_other_user_cannot_delete_someone_elses_checkin(self):
        self.client.login(username="other", password="pass12345")
        resp = self.client.get(f"/checkins/{self.checkin.pk}/delete/")
        self.assertIn(resp.status_code, (403, 404))