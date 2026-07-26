import datetime
import os

import django
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE","DjangoProject1.settings",)
django.setup()

from task.models import SubTask, Task


task_updated = Task.objects.filter(title="Prepare presentation",).update(status=Task.Status.IN_PROGRESS,)

gather_information_updated = SubTask.objects.filter(
    title="Gather information",
    task__title="Prepare presentation",
).update(
    deadline=timezone.now() - datetime.timedelta(days=2),
)

create_slides_updated = SubTask.objects.filter(
    title="Create slides",
    task__title="Prepare presentation",
).update(
    description="Create and format presentation slides",
)

print(f"Updated tasks: {task_updated}")
print(f"Updated Gather information: {gather_information_updated}")
print(f"Updated Create slides: {create_slides_updated}")