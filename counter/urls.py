from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.index, name='index'),
    path('increment/', views.increment, name='increment'),
    path('system_info/', views.system_info, name='system_info'),  # Add system info page
    path('system_info/api/', views.system_info_api, name='system_info_api'),  # Add API endpoint
    path('print/', views.printer_control, name='print'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('stop_feed/', views.stop_feed, name='stop_feed'),
    path('logout_unauth/', auth_views.LogoutView.as_view(), name='logout_auth'),  # Add logout URL
    path('download-image/', views.download_from_external, name='download_from_external'),

]
