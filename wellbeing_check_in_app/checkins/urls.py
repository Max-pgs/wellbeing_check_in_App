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
    path("api/checkins/", views.api_checkins, name="api_checkins"),
    path("goals/", views.goal_list, name="goal_list"),
    path("goals/new/", views.goal_create, name="goal_create"),
    path("goals/<int:goal_id>/edit/", views.goal_update, name="goal_update"),
    path("goals/<int:goal_id>/delete/", views.goal_delete, name="goal_delete"),
    path("habits/", views.habit_list, name="habit_list"),
    path("habits/new/", views.habit_create, name="habit_create"),
    path("habits/<int:habit_id>/edit/", views.habit_update, name="habit_update"),
    path("habits/<int:habit_id>/delete/", views.habit_delete, name="habit_delete"),
]