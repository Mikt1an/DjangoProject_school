from django.urls import path

from .views import TaskCreateView, TaskDetailView, TaskListView, TaskStatisticsView


app_name = "task"
urlpatterns = [
    path("tasks/create/", TaskCreateView.as_view(), name="task-creat"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/statistics/", TaskStatisticsView.as_view(), name="task-statistics"),

]