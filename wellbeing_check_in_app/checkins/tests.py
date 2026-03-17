# Test suite for the wellbeing check-in application.
# These tests cover authentication, CRUD functionality,
# ownership protection, API behaviour, and basic frontend rendering.

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from .models import CheckIn, Goal, Habit



TEST_STATICFILES = override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)


class BaseTestMixin:
    def create_user(self, username="user1", password="pass12345"):
        return User.objects.create_user(username=username, password=password)

    def login(self, username="user1", password="pass12345"):
        return self.client.login(username=username, password=password)

    def create_checkin(
        self,
        user,
        checkin_date=None,
        energy_score=5,
        mood_score=5,
        activity_score=5,
        notes="test checkin",
    ):
        if checkin_date is None:
            checkin_date = date.today()
        return CheckIn.objects.create(
            user=user,
            checkin_date=checkin_date,
            energy_score=energy_score,
            mood_score=mood_score,
            activity_score=activity_score,
            notes=notes,
        )

    def create_goal(
        self,
        user,
        title="Goal 1",
        target_value=10,
        start_date=None,
        end_date=None,
        is_active=True,
    ):
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = date.today() + timedelta(days=7)

        return Goal.objects.create(
            user=user,
            title=title,
            target_value=target_value,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
        )

    def create_habit(
        self,
        user,
        title="Habit 1",
        frequency_type="weekly",
        is_active=True,
    ):
        return Habit.objects.create(
            user=user,
            title=title,
            frequency_type=frequency_type,
            is_active=is_active,
        )

    def assert_redirects_to_login(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["Location"].startswith("/accounts/login/"))

# Tests for authentication and access protection.
@TEST_STATICFILES
class AuthAccessTests(BaseTestMixin, TestCase):
    def test_checkins_requires_login(self):
        resp = self.client.get("/checkins/", follow=False)
        self.assert_redirects_to_login(resp)

    def test_dashboard_requires_login(self):
        resp = self.client.get("/checkins/dashboard/", follow=False)
        self.assert_redirects_to_login(resp)

    def test_progress_requires_login(self):
        resp = self.client.get("/checkins/progress/", follow=False)
        self.assert_redirects_to_login(resp)

    def test_goal_list_requires_login(self):
        resp = self.client.get("/checkins/goals/", follow=False)
        self.assert_redirects_to_login(resp)

    def test_habit_list_requires_login(self):
        resp = self.client.get("/checkins/habits/", follow=False)
        self.assert_redirects_to_login(resp)

    def test_user_can_login(self):
        self.create_user(username="testuser", password="pass12345")
        logged_in = self.client.login(username="testuser", password="pass12345")
        self.assertTrue(logged_in)

# Tests for the user registration flow.
@TEST_STATICFILES
class RegisterTests(BaseTestMixin, TestCase):
    def test_register_page_loads(self):
        resp = self.client.get("/accounts/register/")
        self.assertEqual(resp.status_code, 200)

    def test_user_can_register(self):
        resp = self.client.post(
            "/accounts/register/",
            {
                "username": "newuser123",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp["Location"].startswith("/accounts/login/"))
        self.assertTrue(User.objects.filter(username="newuser123").exists())

# Tests for the user registration flow.
@TEST_STATICFILES
class CheckInCrudTests(BaseTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user(username="owner", password="pass12345")
        self.login(username="owner", password="pass12345")

    def test_owner_can_create_checkin(self):
        before_count = CheckIn.objects.count()

        resp = self.client.post(
            "/checkins/new/",
            {
                "checkin_date": date.today(),
                "energy_score": 7,
                "mood_score": 6,
                "activity_score": 5,
                "notes": "created by owner",
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(CheckIn.objects.count(), before_count + 1)
        self.assertTrue(CheckIn.objects.filter(user=self.user, notes="created by owner").exists())

    def test_owner_can_update_checkin(self):
        checkin = self.create_checkin(self.user, notes="old note")

        resp = self.client.post(
            f"/checkins/{checkin.pk}/edit/",
            {
                "checkin_date": checkin.checkin_date,
                "energy_score": 8,
                "mood_score": 8,
                "activity_score": 7,
                "notes": "updated note",
            },
        )

        self.assertEqual(resp.status_code, 302)
        checkin.refresh_from_db()
        self.assertEqual(checkin.notes, "updated note")
        self.assertEqual(checkin.energy_score, 8)

    def test_owner_can_delete_checkin(self):
        checkin = self.create_checkin(self.user)
        before_count = CheckIn.objects.count()

        resp = self.client.post(f"/checkins/{checkin.pk}/delete/")

        self.assertIn(resp.status_code, [200, 302])
        self.assertEqual(CheckIn.objects.count(), before_count - 1)
        self.assertFalse(CheckIn.objects.filter(pk=checkin.pk).exists())

    def test_checkin_create_invalid_data_returns_errors(self):
        before_count = CheckIn.objects.count()

        resp = self.client.post("/checkins/new/", {})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CheckIn.objects.count(), before_count)

    def test_checkin_list_shows_only_current_users_checkins(self):
        other_user = self.create_user(username="otheruser", password="pass12345")

        self.create_checkin(self.user, checkin_date=date(2026, 3, 10), notes="my checkin")
        self.create_checkin(other_user, checkin_date=date(2026, 3, 1), notes="other checkin")

        resp = self.client.get("/checkins/")
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode()
        self.assertIn("my checkin", content)
        self.assertNotIn("other checkin", content)

# Tests ensuring users cannot access or modify data belonging to other users.
@TEST_STATICFILES
class OwnershipTests(BaseTestMixin, TestCase):
    def setUp(self):
        self.owner = self.create_user(username="owner", password="pass12345")
        self.other = self.create_user(username="other", password="pass12345")

        self.checkin = self.create_checkin(self.owner)
        self.goal = self.create_goal(self.owner, title="Owner Goal")
        self.habit = self.create_habit(self.owner, title="Owner Habit")

        self.login(username="other", password="pass12345")

    def test_other_user_cannot_edit_someone_elses_checkin(self):
        resp = self.client.get(f"/checkins/{self.checkin.pk}/edit/")
        self.assertIn(resp.status_code, [302, 403, 404])

    def test_other_user_cannot_delete_someone_elses_checkin(self):
        resp = self.client.get(f"/checkins/{self.checkin.pk}/delete/")
        self.assertIn(resp.status_code, [302, 403, 404])

    def test_other_user_cannot_edit_someone_elses_goal(self):
        resp = self.client.get(f"/checkins/goals/{self.goal.pk}/edit/")
        self.assertIn(resp.status_code, [302, 403, 404])

    def test_other_user_cannot_delete_someone_elses_goal(self):
        resp = self.client.get(f"/checkins/goals/{self.goal.pk}/delete/")
        self.assertIn(resp.status_code, [302, 403, 404])

    def test_other_user_cannot_edit_someone_elses_habit(self):
        resp = self.client.get(f"/checkins/habits/{self.habit.pk}/edit/")
        self.assertIn(resp.status_code, [302, 403, 404])

    def test_other_user_cannot_delete_someone_elses_habit(self):
        resp = self.client.get(f"/checkins/habits/{self.habit.pk}/delete/")
        self.assertIn(resp.status_code, [302, 403, 404])

# Tests for goal and habit CRUD operations and validation rules.
@TEST_STATICFILES
class GoalHabitCrudAndValidationTests(BaseTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user(username="goaluser", password="pass12345")
        self.login(username="goaluser", password="pass12345")

    def test_goal_invalid_dates_should_fail(self):
        today = date.today()
        yesterday = today - timedelta(days=1)

        resp = self.client.post(
            "/checkins/goals/new/",
            {
                "title": "Bad Goal",
                "target_value": 10,
                "start_date": today,
                "end_date": yesterday,
                "is_active": True,
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "End date cannot be earlier than start date")
        self.assertFalse(Goal.objects.filter(title="Bad Goal").exists())

    def test_owner_can_create_goal(self):
        before_count = Goal.objects.count()

        resp = self.client.post(
            "/checkins/goals/new/",
            {
                "title": "My Goal",
                "target_value": 20,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=5),
                "is_active": True,
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Goal.objects.count(), before_count + 1)
        self.assertTrue(Goal.objects.filter(user=self.user, title="My Goal").exists())

    def test_owner_can_update_goal(self):
        goal = self.create_goal(self.user, title="Old Goal")

        resp = self.client.post(
            f"/checkins/goals/{goal.pk}/edit/",
            {
                "title": "Updated Goal",
                "target_value": 99,
                "start_date": goal.start_date,
                "end_date": goal.end_date,
                "is_active": True,
            },
        )

        self.assertEqual(resp.status_code, 302)
        goal.refresh_from_db()
        self.assertEqual(goal.title, "Updated Goal")
        self.assertEqual(goal.target_value, 99)

    def test_owner_can_delete_goal(self):
        goal = self.create_goal(self.user)
        before_count = Goal.objects.count()

        resp = self.client.post(f"/checkins/goals/{goal.pk}/delete/")

        self.assertIn(resp.status_code, [200, 302])
        self.assertEqual(Goal.objects.count(), before_count - 1)
        self.assertFalse(Goal.objects.filter(pk=goal.pk).exists())

    def test_owner_can_create_habit(self):
        before_count = Habit.objects.count()

        resp = self.client.post(
            "/checkins/habits/new/",
            {
                "title": "Drink Water",
                "frequency_type": "weekly",
                "is_active": True,
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Habit.objects.count(), before_count + 1)
        self.assertTrue(Habit.objects.filter(user=self.user, title="Drink Water").exists())

    def test_owner_can_update_habit(self):
        habit = self.create_habit(self.user, title="Old Habit")

        resp = self.client.post(
            f"/checkins/habits/{habit.pk}/edit/",
            {
                "title": "Updated Habit",
                "frequency_type": "weekly",
                "is_active": True,
            },
        )

        self.assertEqual(resp.status_code, 302)
        habit.refresh_from_db()
        self.assertEqual(habit.title, "Updated Habit")

    def test_owner_can_delete_habit(self):
        habit = self.create_habit(self.user)
        before_count = Habit.objects.count()

        resp = self.client.post(f"/checkins/habits/{habit.pk}/delete/")

        self.assertIn(resp.status_code, [200, 302])
        self.assertEqual(Habit.objects.count(), before_count - 1)
        self.assertFalse(Habit.objects.filter(pk=habit.pk).exists())

# Tests for goal and habit CRUD operations and validation rules.
@TEST_STATICFILES
class ApiTests(BaseTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user(username="apiuser", password="pass12345")
        self.other = self.create_user(username="otherapi", password="pass12345")

        self.create_checkin(
            self.user,
            checkin_date=date(2026, 3, 1),
            energy_score=6,
            mood_score=4,
            activity_score=5,
            notes="mine",
        )
        self.create_checkin(
            self.user,
            checkin_date=date(2026, 3, 2),
            energy_score=8,
            mood_score=6,
            activity_score=7,
            notes="mine too",
        )
        self.create_checkin(
            self.other,
            checkin_date=date(2026, 3, 3),
            energy_score=1,
            mood_score=1,
            activity_score=1,
            notes="other user data",
        )

    def test_api_checkins_requires_login(self):
        resp = self.client.get("/checkins/api/checkins/")
        self.assert_redirects_to_login(resp)

    def test_api_checkins_returns_user_scoped_data(self):
        self.login(username="apiuser", password="pass12345")

        resp = self.client.get("/checkins/api/checkins/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        text = str(data)

        self.assertIn("mine", text)
        self.assertIn("mine too", text)
        self.assertNotIn("other user data", text)

    def test_api_checkins_invalid_date_returns_error(self):
        self.login(username="apiuser", password="pass12345")

        resp = self.client.get("/checkins/api/checkins/?from=not-a-date")
        self.assertNotEqual(resp.status_code, 500)
        self.assertIn(resp.status_code, [400, 302])

    def test_progress_api_requires_login(self):
        resp = self.client.get("/checkins/api/progress/")
        self.assert_redirects_to_login(resp)

    def test_progress_api_returns_expected_shape(self):
        self.login(username="apiuser", password="pass12345")

        resp = self.client.get("/checkins/api/progress/?from=2026-03-01&to=2026-03-03")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()

        self.assertTrue(any(k in data for k in ["summary", "count", "averages"]))
        self.assertTrue(any(k in data for k in ["trends", "trend", "averages", "series"]))
        self.assertTrue(any(k in data for k in ["achievements", "count", "averages", "summary"]))

    def test_progress_api_returns_correct_average_values(self):
        self.login(username="apiuser", password="pass12345")

        resp = self.client.get("/checkins/api/progress/?from=2026-03-01&to=2026-03-03")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()

        self.assertIn("summary", data)

        summary = data["summary"]
        self.assertAlmostEqual(summary.get("avg_energy", 0), 7.0)
        self.assertAlmostEqual(summary.get("avg_mood", 0), 5.0)
        self.assertAlmostEqual(summary.get("avg_activity", 0), 6.0)
        self.assertEqual(summary.get("total_checkins", 0), 2)

    def test_progress_api_invalid_date_returns_error(self):
        self.login(username="apiuser", password="pass12345")

        resp = self.client.get("/checkins/api/progress/?from=not-a-date")
        self.assertEqual(resp.status_code, 400)

# Basic frontend rendering tests to ensure key UI pages load correctly.
@TEST_STATICFILES
class FrontendRenderTests(BaseTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user(username="frontuser", password="pass12345")
        self.login(username="frontuser", password="pass12345")

    def test_dashboard_page_loads_for_logged_in_user(self):
        resp = self.client.get("/checkins/dashboard/")
        self.assertEqual(resp.status_code, 200)

    def test_progress_page_contains_chart_canvas(self):
        resp = self.client.get("/checkins/progress/")
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode().lower()
        self.assertTrue(
            any(keyword in content for keyword in ["canvas", "chart", "progress-chart"])
        )

    def test_history_page_contains_timeline_container(self):
        self.create_checkin(self.user, notes="history item")
        resp = self.client.get("/checkins/")
        self.assertEqual(resp.status_code, 200)

        content = resp.content.decode().lower()
        self.assertTrue(
            any(keyword in content for keyword in ["timeline", "history", "check-ins", "checkins"])
        )