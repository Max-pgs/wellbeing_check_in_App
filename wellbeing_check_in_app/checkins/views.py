from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.contrib.auth.forms import UserCreationForm
from datetime import date, timedelta
from .models import CheckIn, Goal, Habit
from .forms import CheckInForm, GoalForm, HabitForm

# Display the current user's check-ins.
# Filtering by request.user ensures each user only sees their own records.
@login_required
def checkin_list(request):
    checkins = CheckIn.objects.filter(user=request.user)
    return render(request, "checkins/checkin_list.html", {"checkins": checkins})

# Create a new check-in for the authenticated user.
# The user is assigned in the view so it cannot be forged through the form.
@login_required
def checkin_create(request):
    if request.method == "POST":
        form = CheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.user = request.user
            checkin.save()
            return redirect("checkins:checkin_list")
    else:
        form = CheckInForm()

    return render(request, "checkins/checkin_form.html", {"form": form})

# Update an existing check-in owned by the current user.
# get_object_or_404 with user=request.user protects against editing someone else's data.
@login_required
def checkin_update(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk, user=request.user)

    if request.method == "POST":
        form = CheckInForm(request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            return redirect("checkins:checkin_list")
    else:
        form = CheckInForm(instance=checkin)

    return render(request, "checkins/checkin_form.html", {"form": form, "is_update": True})

# Delete a check-in only if it belongs to the current user.
@login_required
def checkin_delete(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk, user=request.user)

    if request.method == "POST":
        checkin.delete()
        return redirect("checkins:checkin_list")

    return render(request, "checkins/checkin_confirm_delete.html", {"checkin": checkin})

# Render the progress page.
# The page structure loads first and the analytics data is fetched later via JavaScript.
@login_required
def progress_view(request):
    return render(request, "checkins/progress.html")

# Render the dashboard page shown after login.
@login_required
def dashboard(request):
    return render(request, "checkins/dashboard.html")

# Display only the goals created by the authenticated user.
@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, "checkins/goal_list.html", {"goals": goals})

# Create a new goal for the current user.
@login_required
def goal_create(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("checkins:goal_list")
    else:
        form = GoalForm()

    return render(request, "checkins/goal_form.html", {"form": form})

# Update a goal only if it belongs to the current user.
@login_required
def goal_update(request, goal_id):
    goal = get_object_or_404(Goal, goal_id=goal_id, user=request.user)

    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect("checkins:goal_list")
    else:
        form = GoalForm(instance=goal)

    return render(request, "checkins/goal_form.html", {"form": form, "goal": goal})

# Delete a goal only if it belongs to the current user.
@login_required
def goal_delete(request, goal_id):
    goal = get_object_or_404(Goal, goal_id=goal_id, user=request.user)

    if request.method == "POST":
        goal.delete()
        return redirect("checkins:goal_list")

    return render(request, "checkins/goal_confirm_delete.html", {"goal": goal})

# Display only the habits created by the authenticated user.
@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, "checkins/habit_list.html", {"habits": habits})

# Create a new habit for the current user.
@login_required
def habit_create(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("checkins:habit_list")
    else:
        form = HabitForm()

    return render(request, "checkins/habit_form.html", {"form": form})

# Update a habit only if it belongs to the current user.
@login_required
def habit_update(request, habit_id):
    habit = get_object_or_404(Habit, habit_id=habit_id, user=request.user)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect("checkins:habit_list")
    else:
        form = HabitForm(instance=habit)

    return render(request, "checkins/habit_form.html", {"form": form, "habit": habit})

# Delete a habit only if it belongs to the current user.
@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, habit_id=habit_id, user=request.user)

    if request.method == "POST":
        habit.delete()
        return redirect("checkins:habit_list")

    return render(request, "checkins/habit_confirm_delete.html", {"habit": habit})

@login_required
def api_progress(request):
    """
    Return analytics data for the authenticated user within a selected date range.

    Query parameters:
    - from: DD-MM-YYYY (optional)
    - to: DD-MM-YYYY (optional)

    If no dates are provided, the API returns data for the last 30 days.
    The response is used by the progress dashboard to render summary cards,
    trend charts, and simple achievement messages.
    """
    qs = CheckIn.objects.filter(user=request.user)

    today = date.today()
    default_from = today - timedelta(days=29)
    default_to = today

    from_str = request.GET.get("from")
    to_str = request.GET.get("to")

    try:
        date_from = date.fromisoformat(from_str) if from_str else default_from
        date_to = date.fromisoformat(to_str) if to_str else default_to
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD for 'from' and 'to'."},
            status=400,
        )

    if date_from > date_to:
        return JsonResponse(
            {"error": "'from' date cannot be after 'to' date."},
            status=400,
        )

    # Restrict analytics to the requested date range for the current user.
    filtered_qs = qs.filter(checkin_date__gte=date_from, checkin_date__lte=date_to).order_by("checkin_date")

    agg = filtered_qs.aggregate(
        count=Count("id"),
        avg_energy=Avg("energy_score"),
        avg_mood=Avg("mood_score"),
        avg_activity=Avg("activity_score"),
    )

    def r1(value):
        return round(float(value), 1) if value is not None else None

    trends = [
        {
            "label": checkin.checkin_date.isoformat(),
            "date": checkin.checkin_date.isoformat(),
            "energy": checkin.energy_score,
            "mood": checkin.mood_score,
            "activity": checkin.activity_score,
        }
        for checkin in filtered_qs
    ]

    # Generate simple achievement messages based on check-in consistency
    # and strong average wellbeing scores.
    achievements = []
    count = agg["count"] or 0

    if count >= 3:
        achievements.append("3 check-ins in this period. Good start")
    if count >= 7:
        achievements.append("7 check-ins in this period. Consistent effort")
    if count >= 12:
        achievements.append("12 check-ins in this period. Great dedication")

    if agg["avg_mood"] and agg["avg_mood"] >= 8:
        achievements.append("High mood average")
    if agg["avg_energy"] and agg["avg_energy"] >= 8:
        achievements.append("Strong energy average")
    if agg["avg_activity"] and agg["avg_activity"] >= 8:
        achievements.append("High activity average")

    payload = {
        "from": date_from.isoformat(),
        "to": date_to.isoformat(),
        "summary": {
            "avg_energy": r1(agg["avg_energy"]),
            "avg_mood": r1(agg["avg_mood"]),
            "avg_activity": r1(agg["avg_activity"]),
            "total_checkins": count,
        },
        "trends": trends,
        "achievements": achievements,
    }

    return JsonResponse(payload)

@login_required
def api_checkins(request):
    """
    Returns check-ins for the current user over a date range.
    Query params:
      - from: DD-MM-YYYY (optional)
      - to:   DD-MM-YYYY (optional)
    Defaults to last 30 days inclusive.
    """
    qs = CheckIn.objects.filter(user=request.user)

    today = date.today()
    default_from = today - timedelta(days=29)
    default_to = today

    from_str = request.GET.get("from")
    to_str = request.GET.get("to")

    try:
        date_from = date.fromisoformat(from_str) if from_str else default_from
        date_to = date.fromisoformat(to_str) if to_str else default_to
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD for 'from' and 'to'."},
            status=400,
        )

    if date_from > date_to:
        return JsonResponse(
            {"error": "'from' date cannot be after 'to' date."},
            status=400,
        )

    # Return only the current user's check-ins within the requested date window
    qs = qs.filter(checkin_date__gte=date_from, checkin_date__lte=date_to)

    # Keep the payload simple so the history timeline can render records directly in JavaScript
    data = [
        {
            "id": c.id,
            "checkin_date": c.checkin_date.isoformat(),
            "energy_score": c.energy_score,
            "mood_score": c.mood_score,
            "activity_score": c.activity_score,
            "notes": c.notes,
        }
        for c in qs
    ]

    return JsonResponse(
        {"from": date_from.isoformat(), "to": date_to.isoformat(), "count": len(data), "items": data}
    )

# Register a new user with Django's built-in authentication form
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html",{"form":form})

