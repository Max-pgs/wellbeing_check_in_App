from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
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