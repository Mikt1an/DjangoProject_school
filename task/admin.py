from django.contrib import admin
from .models import Category, Task, SubTask

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "deadline", "created_at",)
    list_filter = ("status", "category", "deadline", "created_at",)
    search_fields = ("title", "description",)
    filter_horizontal = ("category",)
    readonly_fields = ("created_at",)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at",)
    list_filter = ("status", "task", "deadline", "created_at",)
    search_fields = ("title", "description", "task__title",)
    readonly_fields = ("created_at",)