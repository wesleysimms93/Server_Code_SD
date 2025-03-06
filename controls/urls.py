from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Manual/', views.manual_control, name='manual_control'),  # Add system info page
    path('download-image/', views.download_from_external, name='download_from_external'),
]
