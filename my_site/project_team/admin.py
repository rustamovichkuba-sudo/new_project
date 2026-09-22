from django.contrib import admin
from django.contrib import admin
from .models import (
    UserProfile,
    Category,
    Project,
    Tag,
    Task,
    Subtask,
    TaskFile,
    Comment,
    Favorite,
    FavoriteItem,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'phone_number', 'status')
    search_fields = ('username', 'phone_number')
    list_filter = ('status',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'category', 'owner')
    list_filter = ('category',)


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project',
        'priority',
        'completed',
        'deadline',
    )
    search_fields = ('title',)
    list_filter = (
        'priority',
        'completed',
        'project',
    )
    inlines = [
        SubtaskInline,
        TaskFileInline,
        CommentInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('tag_name',)


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'completed')


@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task', 'file')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_date')
    search_fields = ('text',)


class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    inlines = [FavoriteItemInline]


@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('favorite', 'task')

