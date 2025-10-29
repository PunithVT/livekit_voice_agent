from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Module, Lesson, UserProgress, UserNote
from .serializers import (
    ModuleSerializer, 
    LessonSerializer,
    UserProgressSerializer,
    UserNoteSerializer
)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.filter(is_active=True).order_by('order')
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        module_slug = self.request.query_params.get('module', None)
        if module_slug:
            queryset = queryset.filter(module__slug=module_slug)
        return queryset.order_by('order')

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserNoteViewSet(viewsets.ModelViewSet):
    serializer_class = UserNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)