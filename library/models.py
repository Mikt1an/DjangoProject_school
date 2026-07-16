from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg

from decimal import Decimal



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Author(TimeStampedModel):
    f_name = models.CharField(max_length=100, verbose_name="author's name")
    l_name = models.CharField(max_length=100, verbose_name="author's last name")
    birth_date = models.DateField(verbose_name="birth date")

    profile = models.URLField(null=True, blank=True, verbose_name="profile url")
    deleted = models.BooleanField(default=False, verbose_name="deleted")
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="rating",
    )

    def __str__(self):
        last_name_initial = (
            f"{self.l_name[0]}."
            if self.l_name
            else ""
        )
        return f"{self.f_name} {last_name_initial}".strip()


class Member(TimeStampedModel):

    class Gender(models.TextChoices):
        MALE = "male", "male"
        FEMALE = "female", "female"
        OTHER = "other", "other"


    class Role(models.TextChoices):
        ADMIN = "admin", "admin"
        EMPLOYER = "employer", "employer"
        READER = "reader", "reader"


    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=50, verbose_name="last name")

    email = models.EmailField(null=True, unique=True, verbose_name="email address")

    gender = models.CharField(max_length=10, choices=Gender.choices)

    birth_date = models.DateField(max_length=10, blank=True, verbose_name="birth date")

    age = models.PositiveIntegerField(validators=[MinValueValidator(6), MaxValueValidator(120)], verbose_name="age")

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.READER, verbose_name="role")

    is_active = models.BooleanField(default=True, verbose_name="is active")

    library = models.ManyToManyField("Library", blank=True, related_name="members")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="category's name")

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    title = models.CharField(max_length=100, verbose_name="title")
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    publish_date = models.DateField(verbose_name="publish date")

    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Romance', 'Romance'),
        ('Children', 'Children'),
        ('Horror', 'Horror'),
        ("Health", "Health"),
        ('Adventure', 'Adventure'),
        ('Manga', 'Manga'),
    ]

    description = models.TextField(null=True, blank=True, verbose_name="description")
    genre = models.CharField(null=True, blank=True, max_length=100, choices=GENRE_CHOICES)
    pages = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10000)])

    publisher = models.ForeignKey(
        "Member",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_books",
        limit_choices_to={
            "role__in": ["admin", "employee"],
            },
        verbose_name="published_books",
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books",)

    @property
    def rating(self):
        average_rating = self.reviews.aggregate(Avg("rating"))["rating__avg"]

        if average_rating is None:
            return 0

        return round(average_rating, 2)

    def __str__(self):
        return self.title


class Library(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="name")
    location = models.CharField(max_length=100, null=True, verbose_name="location")
    website = models.URLField(null=True, blank=True, verbose_name="website")

    books = models.ManyToManyField("Book", blank=True, related_name="libraries",)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique_for_date="created_at")
    text = models.TextField()

    author = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="posts")

    is_moderated = models.BooleanField(default=False)

    library = models.ForeignKey("Library", on_delete=models.CASCADE, related_name="posts")

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Borrow(TimeStampedModel):
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="borrows")

    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="borrows")

    library = models.ForeignKey("Library", on_delete=models.CASCADE, related_name="borrows")

    borrow_date = models.DateField()
    return_date = models.DateField()

    is_returned = models.BooleanField(default=False)

    def is_overdue(self):
        return (
            not self.is_returned
            and self.return_date < timezone.localdate()
        )

    def __str__(self):
        return f"{self.member} — {self.book}"


class Review(TimeStampedModel):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="reviews")
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("1.0")),
            MaxValueValidator(Decimal("5.0"))
        ]
    )

    review = models.TextField()

    def __str__(self):
        return f"{self.book} — {self.rating}"


class AuthorDetail(TimeStampedModel):
    author = models.OneToOneField("Author", on_delete=models.CASCADE, related_name="details")

    biography = models.TextField()
    birth_city = models.CharField(max_length=100, null=True, blank=True, verbose_name="birth city")
    gender = models.CharField(max_length=10, choices=Member.Gender.choices)

    def __str__(self):
        return f"Additionally data: {self.author}"


class Event(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name="title")
    description = models.TextField()
    event_date = models.DateField()
    library = models.ForeignKey("Library", on_delete=models.CASCADE, related_name="events")
    books = models.ManyToManyField("Book", related_name="events", blank=True)
    participants = models.ManyToManyField("Member", through="EventParticipant", related_name="events", blank=True)

    def __str__(self):
        return (
            f"{self.title} — "
            f"{self.library}, "
            f"{self.event_date:%d.%m.%Y %H:%M}"
        )

    class Meta:
        ordering = ["event_date"]


class EventParticipant(TimeStampedModel):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="registrations")
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="event_registrations")
    registration_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return (
            f"{self.member} - {self.event.title}"
            f"{self.registration_date:%d.%m.%Y %H:%M}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event", "member"],
                name="unique_event_member_registration",
            )
        ]
        ordering = ["registration_date"]