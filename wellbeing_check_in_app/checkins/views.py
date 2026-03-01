from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count
from datetime import date, timedelta
from .models import CheckIn
from .forms import CheckInForm


@login_required
def checkin_list(request):
    checkins = CheckIn.objects.filter(user=request.user)
    return render(request, "checkins/checkin_list.html", {"checkins": checkins})


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

@login_required
def checkin_delete(request, pk):
    checkin = get_object_or_404(CheckIn, pk=pk, user=request.user)

    if request.method == "POST":
        checkin.delete()
        return redirect("checkins:checkin_list")

    return render(request, "checkins/checkin_confirm_delete.html", {"checkin": checkin})

@login_required
def progress_view(request):
    return render(request, "checkins/progress.html")

@login_required
def api_progress(request):
    """
    Returns averages for the current user over a date range.
    Query params:
      - from: YYYY-MM-DD (optional)
      - to:   YYYY-MM-DD (optional)
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
        date_from, date_to = date_to, date_from

    qs = qs.filter(checkin_date__gte=date_from, checkin_date__lte=date_to)

    agg = qs.aggregate(
        count=Count("id"),
        avg_energy=Avg("energy_score"),
        avg_mood=Avg("mood_score"),
        avg_activity=Avg("activity_score"),
    )

    def r1(x):
        return round(float(x), 1) if x is not None else None

    payload = {
        "from": date_from.isoformat(),
        "to": date_to.isoformat(),
        "count": agg["count"],
        "averages": {
            "energy": r1(agg["avg_energy"]),
            "mood": r1(agg["avg_mood"]),
            "activity": r1(agg["avg_activity"]),
        },
    }
    return JsonResponse(payload)

@login_required
def api_checkins(request):
    """
    Returns check-ins for the current user over a date range.
    Query params:
      - from: YYYY-MM-DD (optional)
      - to:   YYYY-MM-DD (optional)
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
        date_from, date_to = date_to, date_from

    qs = qs.filter(checkin_date__gte=date_from, checkin_date__lte=date_to)

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

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html",{"form":form})