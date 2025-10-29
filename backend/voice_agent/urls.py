from django.urls import path
from . import views

urlpatterns = [
    path('get-token/', views.get_token, name='voice_get_token'),
    path('config/', views.get_config, name='voice_config'),
]
