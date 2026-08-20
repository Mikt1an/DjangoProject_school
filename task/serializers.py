from django.utils import timezone
from rest_framework import serializers

from .models import Task, Category, SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source="task.title", read_only=True)
    class Meta:
        model = SubTask
        fields = (
            "id",
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at",
        )
        read_only_fields = ("id",)


class SubTaskCreateSerializer(SubTaskSerializer):
    created_at = serializers.DateTimeField(read_only=True)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        name = validated_data["name"]

        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError(
                {
                    "name": "Category with this name already exists."
                }
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)

        category_exists = (
            Category.objects
            .filter(name__iexact=name)
            .exclude(pk=instance.pk)
            .exists()
        )

        if category_exists:
            raise serializers.ValidationError(
                {
                    "name": "Category with this name already exists."
                }
            )

        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "deadline",
        )
        read_only_fields = ("id",)


class TaskCreateSerializer(TaskSerializer):
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Deadline cannot be in the past."
            )

        return value


class TaskDetailSerializer(TaskSerializer):
    subtasks = SubTaskSerializer(
        many=True,
        read_only=True,
    )

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ("subtasks",)