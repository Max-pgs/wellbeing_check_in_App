from django.conf import settings
from django.db import models

class CheckIn(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="checkins",
    )

    checkin_date = models.DateField()

    energy_score = models.PositiveSmallIntegerField()
    mood_score = models.PositiveSmallIntegerField()
    activity_score = models.PositiveSmallIntegerField()

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-checkin_date", "-created_at"]

    def __str__(self):
        return f"{self.user} - {self.checkin_date}"
