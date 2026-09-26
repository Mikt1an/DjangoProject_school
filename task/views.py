from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, SubTask
from .pagination import SubTaskPagination
from .serializers import (
    SubTaskCreateSerializer,
    SubTaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskSerializer,
)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskListView(ListAPIView):
    serializer_class = TaskSerializer

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


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


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
    pagination_class = SubTaskPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer

        return SubTaskSerializer

    def get_queryset(self):
        queryset = (
            SubTask.objects
            .all()
            .order_by("-created_at")
        )

        task_title = self.request.query_params.get("task_title")
        subtask_status = self.request.query_params.get("status")

        if task_title:
            queryset = queryset.filter(
                task__title__iexact=task_title,
            )

        if subtask_status:
            queryset = queryset.filter(
                status=subtask_status,
            )

        return queryset


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(
            SubTask,
            pk=pk,
        )

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        subtask = self.get_object(pk)

        serializer = SubTaskCreateSerializer(
            subtask,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, pk):
        subtask = self.get_object(pk)

        serializer = SubTaskCreateSerializer(
            subtask,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )