from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


# Create your models here.
class Category(TimeStampModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_category_name",
            ),
        ]

    def __str__(self):
        return self.name


class Task(TimeStampModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in-progress", "In Progress"
        PENDING = "pending", "Pending"
        BLOCKED = "blocked", "Blocked"
        DONE = "done", "Done"

    title = models.CharField(max_length=200, unique_for_date='deadline',)
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category, related_name='tasks', blank=True)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                name="unique_task_title",
            ),
        ]

    def __str__(self):
        return self.title


class SubTask(TimeStampModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        PENDING = "pending", "Pending"
        BLOCKED = "blocked", "Blocked"
        DONE = "done", "Done"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["-created_at"]
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"

        constraints = [
            models.UniqueConstraint(
                fields=["title"],
                name="unique_subtask_title",
            ),
        ]

    def __str__(self):
        return self.title