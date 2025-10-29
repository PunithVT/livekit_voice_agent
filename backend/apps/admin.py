from django.contrib import admin
from .models import Module, Lesson, UserProgress, UserNote

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_exercise')
    list_filter = ('module', 'is_exercise')
    list_editable = ('order', 'is_exercise')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'last_accessed')
    list_filter = ('completed', 'lesson__module')

@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'updated_at')
    list_filter = ('user', 'lesson__module')