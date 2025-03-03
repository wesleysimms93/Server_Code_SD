# images/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('download/<str:filename>/', views.download_image, name='download_image'),  # Download page
]
