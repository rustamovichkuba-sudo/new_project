from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def validate_age(value):
    if value < 14 or value > 70:
        raise ValidationError(
            'Возраст должен быть в диапазоне от 14 до 70 лет.'
        )


class UserProfile(AbstractUser):
    STATUS_CHOICES = [
        ('beginner', 'Beginner'),
        ('active', 'Active'),
        ('pro', 'Pro'),
    ]

    age = models.PositiveSmallIntegerField(
        validators=[validate_age],
        null=True,
        blank=True
    )
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='beginner'
    )
    date_register = models.DateField(auto_now_add=True)

    def str(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(
        max_length=50,
        unique=True
    )
    category_img = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    def str(self):
        return self.category_name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.project_name

    def get_tasks_count(self):
        return self.tasks.count()

    def get_completed_percent(self):
        total_tasks = self.get_tasks_count()

        if total_tasks == 0:
            return 0

        completed_tasks = self.tasks.filter(
            completed=True
        ).count()

        return int((completed_tasks / total_tasks) * 100)