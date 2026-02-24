from django.urls import path
from . import views

app_name = "checkins"

urlpatterns = [
    path("", views.checkin_list, name="checkin_list"),
    path("new/", views.checkin_create, name="checkin_create"),
    path("<int:pk>/edit/", views.checkin_update, name="checkin_update"),
    path("<int:pk>/delete/", views.checkin_delete, name="checkin_delete"),
    path("api/progress/", views.api_progress, name="api_progress"),
    path("progress/", views.progress_view, name="progress"),
]