from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Data models for the wellbeing check-in application.
# Each model is linked to the authenticated user so that every user
# only sees and manages their own records.


# Stores one wellbeing check-in entry for a specific day.
# Scores are kept on a 0-10 scale to support simple tracking and analytics.
class CheckIn(models.Model):
    
    # Link each check-in to the user who created it.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="checkins",
    )
    
    # The date the wellbeing record refers to.
    checkin_date = models.DateField(
        verbose_name="Check-in date"
    )

    # Numeric wellbeing metrics used in charts and summary statistics.
    energy_score = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    mood_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    activity_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Optional free-text notes that give extra context to the check-in.
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Show most recent check-ins first in the interface.
    class Meta:
        ordering = ["-checkin_date", "-created_at"]

    def __str__(self):
        return f"{self.user} - {self.checkin_date}"

# Stores a personal goal created by a user.
# Goals include a target value and a date range so progress can be tracked over time.
class Goal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals"
    )
    title = models.CharField(max_length=255)
    target_value = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date", "-goal_id"]

    def __str__(self):
        return self.title

# Stores a habit the user wants to track.
# Frequency type is used to describe how often the habit should be repeated.
class Habit(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    FREQUENCY_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
    ]

    habit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits"
    )
    title = models.CharField(max_length=255)
    frequency_type = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at", "-habit_id"]

    def __str__(self):
        return self.title
