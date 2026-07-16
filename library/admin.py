from django.contrib import admin
from .models import Book, Library

from .models import (
    Author,
    AuthorDetail,
    Borrow,
    # Book,
    Category,
    Event,
    EventParticipant,
    Library,
    Member,
    Post,
    Review,
)


admin.site.register(
    [
        Author,
        AuthorDetail,
        Category,
        EventParticipant,
        Library,
        Member,
        Review,
    ]
)


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "average_rating",
        "show_libraries",
    )

    readonly_fields = (
        "average_rating",
        "show_libraries",
    )

    @admin.display(description="average_rating")
    def average_rating(self, obj):
        if not obj or not obj.pk:
            return "No rewiews"

        if obj.rating == 0:
            return "No rating"

        return f"{obj.rating:.2f}"

    @admin.display(description="Libraries")
    def show_libraries(self, obj):
        if not obj.pk:
            return "First save book"

        libraries = obj.libraries.all()

        if not libraries:
            return "book is not have"

        return ", ".join(
            library.name for library in libraries
        )


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "book",
        "library",
        "borrow_date",
        "return_date",
        "is_returned",
        "overdue_status",
    )

    @admin.display(
        description="overdue",
        boolean=True,
    )
    def overdue_status(self, obj):
        return obj.is_overdue()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "library",
        "event_date",
        "participants_count",
    )

    filter_horizontal = ("books",)
    inlines = (EventParticipantInline,)

    @admin.display(description="Участников")
    def participants_count(self, obj):
        return obj.participants.count()


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "library",
        "is_moderated",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_moderated",
        "library",
        "created_at",
    )

    search_fields = (
        "title",
        "text",
    )

    readonly_fields = (
        "updated_at",
    )