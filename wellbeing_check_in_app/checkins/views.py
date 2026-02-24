from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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