from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProgress, Lesson

@receiver(post_save, sender=UserProgress)
def update_module_progress(sender, instance, created, **kwargs):
    """
    Update module completion status when all lessons are completed
    """
    if instance.completed:
        # Check if all lessons in the module are completed
        module = instance.lesson.module
        total_lessons = module.lessons.count()
        completed_lessons = UserProgress.objects.filter(
            user=instance.user,
            lesson__module=module,
            completed=True
        ).count()
        
        # You can add logic here to mark module as completed
        # if completed_lessons == total_lessons