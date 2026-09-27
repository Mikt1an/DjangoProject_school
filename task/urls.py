from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    TaskDetailUpdateDeleteView,
    TaskListCreateView,
    TaskStatisticsView,
)


router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)


urlpatterns = [
    path(
        "tasks/",
        TaskListCreateView.as_view(),
        name="task-list-create",
    ),
    path(
        "tasks/statistics/",
        TaskStatisticsView.as_view(),
        name="task-statistics",
    ),
    path(
        "tasks/<int:pk>/",
        TaskDetailUpdateDeleteView.as_view(),
        name="task-detail",
    ),
    path(
        "subtasks/",
        SubTaskListCreateView.as_view(),
        name="subtask-list-create",
    ),
    path(
        "subtasks/<int:pk>/",
        SubTaskDetailUpdateDeleteView.as_view(),
        name="subtask-detail",
    ),
]

urlpatterns += router.urls