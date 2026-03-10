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
        }
        
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = [
            "title", 
            "target_value", 
            "start_date", 
            "end_date", 
            "is_active"
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "title", 
            "frequency_type", 
            "is_active"]