import os

import django
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE","DjangoProject1.settings",)
django.setup()

from task.models import SubTask, Task


new_tasks = Task.objects.filter(
    status=Task.Status.NEW,
)

print("Tasks with New status:")

for task in new_tasks:
    print(
        task.title,
        task.get_status_display(),
        task.deadline,
    )


overdue_done_subtasks = SubTask.objects.filter(
    status=SubTask.Status.DONE,
    deadline__lt=timezone.now(),
)

print("\nOverdue subtasks with Done status:")

for subtask in overdue_done_subtasks:
    print(
        subtask.title,
        subtask.get_status_display(),
        subtask.deadline,
    )