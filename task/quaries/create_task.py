import datetime
import os

import django
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE","DjangoProject1.settings",)
django.setup()

from task.models import SubTask, Task


current_datetime = timezone.now()

Task.objects.filter(
    title="Prepare presentation",
).delete()

SubTask.objects.filter(
    title__in=[
        "Gather information",
        "Create slides",
    ],
).delete()


task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status=Task.Status.NEW,
    deadline=current_datetime + datetime.timedelta(days=3),
)

gather_information = SubTask.objects.create(
    task=task,
    title="Gather information",
    description="Find necessary information for the presentation",
    status=SubTask.Status.NEW,
    deadline=current_datetime + datetime.timedelta(days=2),
)

create_slides = SubTask.objects.create(
    task=task,
    title="Create slides",
    description="Create presentation slides",
    status=SubTask.Status.NEW,
    deadline=current_datetime + datetime.timedelta(days=1),
)


print("Task created:")
print(
    task.title,
    task.get_status_display(),
    task.deadline,
)

print("\nSubtasks created:")

for subtask in task.subtasks.all():
    print(
        subtask.title,
        subtask.get_status_display(),
        subtask.deadline,
    )