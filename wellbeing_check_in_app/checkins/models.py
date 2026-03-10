from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="checkins",
    )

    checkin_date = models.DateField()

    energy_score = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    mood_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    activity_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-checkin_date", "-created_at"]

    def __str__(self):
        return f"{self.user} - {self.checkin_date}"
    
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
