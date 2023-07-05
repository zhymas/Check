from django.urls import path, include
from .views import create_check

urlpatterns = [
    path('create-check/', create_check, name='create_check')
]
