from django.db.models import Count, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Task, Category, SubTask
from .serializers import (
    CategoryCreateSerializer,
    SubTaskCreateSerializer,
    SubTaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskSerializer,
)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "deadline",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer

        return TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()

        weekday = self.request.query_params.get("weekday")

        if weekday:
            weekdays = {
                "sunday": 1,
                "monday": 2,
                "tuesday": 3,
                "wednesday": 4,
                "thursday": 5,
                "friday": 6,
                "saturday": 7,
            }

            weekday_number = weekdays.get(weekday.lower())

            if weekday_number:
                queryset = queryset.filter(
                    deadline__week_day=weekday_number,
                )

        return queryset


class TaskDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return TaskCreateSerializer

        return TaskDetailSerializer


class TaskStatisticsView(APIView):
    def get(self, request):
        summary = Task.objects.aggregate(
            total_tasks=Count("id"),
            overdue_tasks=Count(
                "id",
                filter=Q(deadline__lt=timezone.now()),
            ),
        )

        status_rows = (
            Task.objects
            .values("status")
            .annotate(count=Count("id"))
            .order_by()
        )

        status_counts = {
            value: 0
            for value, _ in Task._meta.get_field("status").choices
        }

        status_counts.update(
            {
                row["status"]: row["count"]
                for row in status_rows
            }
        )

        return Response(
            {
                "total_tasks": summary["total_tasks"],
                "tasks_by_status": status_counts,
                "overdue_tasks": summary["overdue_tasks"],
            },
            status=status.HTTP_200_OK,
        )


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "deadline",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer

        return SubTaskSerializer

    def get_queryset(self):
        queryset = SubTask.objects.all()

        task_title = self.request.query_params.get("task_title")

        if task_title:
            queryset = queryset.filter(
                task__title__iexact=task_title,
            )

        return queryset


class SubTaskDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return SubTaskCreateSerializer

        return SubTaskSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(
        detail=True,
        methods=["get"],
    )
    def count_tasks(self, request, pk=None):
        category = self.get_object()

        return Response(
            {
                "category": category.name,
                "tasks_count": category.tasks.count(),
            },
            status=status.HTTP_200_OK,
        )