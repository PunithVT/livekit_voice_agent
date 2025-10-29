from rest_framework import serializers
from .models import Module, Lesson, UserProgress, UserNote

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['module']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['user', 'last_accessed']

class UserNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNote
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']