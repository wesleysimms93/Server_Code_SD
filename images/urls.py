# images/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('download/<str:filename>/', views.download_image, name='download_image'),  # Download page
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/<str:folder_name>/', views.image_list_folder, name='folder_image_list'),
    path('download_folder/<str:filename>/', views.download_image_folder, name='folder_download')
]
