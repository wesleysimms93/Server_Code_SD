from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Manual/', views.manual_control, name='manual_control'),  # Add system info page
    path('download-image/', views.download_from_external, name='download_from_external'),
    path('download-image-IR/', views.download_from_external_IR, name='download_from_external_IR'),
    path('download-image-VL/', views.download_from_external_VL, name='download_from_external_VL'),
    path('video/', views.video_stream, name='video_stream'),
    #path('Manual/execute/<str:action>/', views.execute_cool_script, name='execute_cool_script'),
    #path('Manual/execute_cool_script/<str:action>/', views.execute_cool_script, name='execute_cool_script'),
    path('automatic-control/', views.automatic_control, name='automatic_control'),
]
