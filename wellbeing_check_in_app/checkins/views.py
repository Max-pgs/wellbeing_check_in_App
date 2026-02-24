from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
            return redirect("checkin_list")
    else:
        form = CheckInForm()

    return render(request, "checkins/checkin_form.html", {"form": form})