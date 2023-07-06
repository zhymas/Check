from django.urls import path, include
from .views import create_check, print_checks

urlpatterns = [
    path('create-check/', create_check, name='create_check'),
    path('print-check/', print_checks, name='print-check'),
]
