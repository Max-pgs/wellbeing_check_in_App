from django.urls import path
from . import views

urlpatterns = [
    path("checkins/", views.checkin_list, name="checkin_list"),
    path("checkins/new/", views.checkin_create, name="checkin_create"),
]