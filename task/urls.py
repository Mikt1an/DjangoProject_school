from django.urls import path

from .views import (
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    TaskCreateView, TaskDetailView, TaskListView, TaskStatisticsView
)


app_name = "task"
urlpatterns = [
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/statistics/", TaskStatisticsView.as_view(), name="task-statistics"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view(), name="subtask-detail"),

]