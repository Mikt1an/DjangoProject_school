import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE","DjangoProject1.settings",)
django.setup()

from task.models import SubTask, Task


task = Task.objects.filter(title="Prepare presentation",).first()

if task:
    subtasks_count = task.subtasks.count()
    deleted_count, deleted_details = task.delete()
    print(f"Related subtasks: {subtasks_count}")
    print(f"Deleted objects: {deleted_count}")
    print(f"Deletion details: {deleted_details}")
else:
    print("Task not found.")


task_exists = Task.objects.filter(title="Prepare presentation",).exists()

subtasks_exist = SubTask.objects.filter(
    title__in=[
        "Gather information",
        "Create slides",
    ],
).exists()

print(f"Task exists: {task_exists}")
print(f"Subtasks exist: {subtasks_exist}")