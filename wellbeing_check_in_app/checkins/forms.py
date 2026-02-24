from django import forms
from .models import CheckIn


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = [
            "checkin_date",
            "energy_score",
            "mood_score",
            "activity_score",
            "notes",
        ]