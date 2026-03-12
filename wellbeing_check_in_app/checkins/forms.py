from django import forms
from .models import CheckIn, Goal, Habit


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

        widgets = {
            "checkin_date": forms.DateInput(attrs={"type": "date"}),

            "energy_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "value": 5,
                    "step": 1,
                }
            ),

            "mood_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "value": 5,
                    "step": 1,
                }
            ),

            "activity_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 1,
                    "max": 10,
                    "value": 5,
                    "step": 1,
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Add any additional thoughts..."
                }
            ),
        }
