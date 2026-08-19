from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer

# Create your views here.
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all().order_by("id")
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


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
            }
        )