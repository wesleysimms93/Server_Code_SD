from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
#from Orvar import urls
#from controls import views

urlpatterns = [
    path('server_info/', views.system_info, name='system_info'),  # Add system info page
    path('system_info/api/', views.system_info_api, name='system_info_api'),  # Add API endpoint
    path('', views.index, name='home')
]
    
