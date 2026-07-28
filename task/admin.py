from django.contrib import admin
from .models import Category, Task, SubTask

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("name",)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_title",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = (
        "status",
        "deadline",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
    )
    filter_horizontal = ("category",)
    ordering = ("-created_at",)

    inlines = (SubTaskInline,)


    @admin.display(description="Title", ordering="title")
    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "task",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = (
        "status",
        "deadline",
        "created_at",
    )
    search_fields = ("title", "description", "task__title",)
    ordering = ("-created_at",)

    actions = ("mark_as_done",)

    @admin.action(description="Mark selected subtasks as Done")
    def mark_as_done(self, request, queryset):
        updated_count = queryset.update(status=SubTask.Status.DONE)

        self.message_user(
            request,
            f"{updated_count} subtask(s) marked as Done.",
        )