from django.db import models
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



class TaskFile(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="files",
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="task_files/")

    def __str__(self):
        return f"Файл для задачи: {self.task}"


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="comments",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий {self.user} к {self.task}"


class Favorite(models.Model):
    user = models.OneToOneField(
        UserProfile,
        related_name="favorite",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Избранное пользователя {self.user}"


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(
        Favorite,
        related_name="items",
        on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["favorite", "task"],
                name="unique_favorite_task"
            )
        ]

    def __str__(self):
        return f"{self.task} в избранном {self.favorite.user}"
