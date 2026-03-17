from django import forms
from .models import CheckIn, Goal, Habit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from datetime import date

# Custom login view that uses the project's custom authentication form
# and renders the login template with email/password fields.
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your username",
            "autocomplete": "username",
            "autofocus": True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        })
    )

# Custom registration form extending Django's UserCreationForm.
# Adds custom placeholders and help text for username and password fields.
# Validates password strength and ensures password confirmation matches.
class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        help_text="150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your username",
            "autocomplete": "username",
            "autofocus": True
        })
    )

    password1 = forms.CharField(
        help_text=UserCreationForm.base_fields['password1'].help_text,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "autocomplete": "new-password"
        })
    )

    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Re-enter your password",
            "autocomplete": "new-password"
        })
    )

# Form for creating and updating daily wellbeing check-ins.
# Uses HTML5 range sliders for energy, mood, and activity scores (0-10 scale).
# Includes date validation to prevent check-ins from future dates.
# User assignment is handled in the view to prevent data forgery.
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

        # Use HTML5 inputs and sliders to make the form easier to complete.
        widgets = {
            "checkin_date": forms.DateInput(attrs={"type": "date"}),

            "energy_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 0,
                    "max": 10,
                    "value": 5,
                    "step": 1,
                }
            ),

            "mood_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 0,
                    "max": 10,
                    "value": 5,
                    "step": 1,
                }
            ),

            "activity_score": forms.NumberInput(
                attrs={
                    "type": "range",
                    "min": 0,
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
        
    def clean_checkin_date(self):
        checkin_date = self.cleaned_data.get("checkin_date")

        if checkin_date and checkin_date > date.today():
            raise forms.ValidationError(
                "Check-ins cannot be created for future dates."
            )

        return checkin_date

# Form for creating and editing goals.
# Includes additional validation to ensure the date range is logical.
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
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Walk 8,000 steps a day"}
            ),
            "target_value": forms.NumberInput(
                attrs={"placeholder": "e.g. 30"}
            ),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
        
    # Prevent users from saving a goal whose end date is before the start date.
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                "End date cannot be earlier than start date."
            )

        return cleaned_data
    

# Form for creating and editing habits.
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = [
            "title", 
            "frequency_type", 
            "is_active"
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Walk 8,000 steps a day"}
            ),
            "target_value": forms.NumberInput(
                attrs={"placeholder": "e.g. 30"}
            )
        }