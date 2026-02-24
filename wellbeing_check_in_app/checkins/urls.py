from django.urls import path, include
from . import views

urlpatterns = [
    path("checkins/", views.checkin_list, name="checkin_list"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("checkins/new/", views.checkin_create, name="checkin_create"),
]