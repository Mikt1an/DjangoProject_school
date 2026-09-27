from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CurrentUserTaskListView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    TaskDetailUpdateDeleteView,
    TaskListCreateView,
    TaskStatisticsView,
)
from .auth_views import (
    LoginView,
    LogoutView,
    RefreshView,
    RegisterView,
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
        "tasks/my/",
        CurrentUserTaskListView.as_view(),
        name="current-user-tasks",
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
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "auth/login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "auth/refresh/",
        RefreshView.as_view(),
        name="refresh",
    ),

    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

urlpatterns += router.urls