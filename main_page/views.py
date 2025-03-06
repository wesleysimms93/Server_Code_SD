from django.shortcuts import render, redirect
from django.http import JsonResponse
import psutil
from django.contrib.auth.decorators import login_required
import cv2
import io
import os
import time
import numpy as np
import requests
from datetime import datetime
import threading
from picamera2 import Picamera2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from controls import views


# Global variable to control the camera feed thread
camera_thread = None
feed_active = False
picam2 = None
test = 0;
media_dir = os.path.join(os.getcwd(), 'media/pictures')

#Global URL for the Camera Checked when the system requests the location 
Camera_URL = "http://192.168.100.2:5000"


@login_required
def index(request):
    return render(request, 'index.html')

# Create your views here.
@login_required
def system_info(request):
    # Gather system information
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    # Get the temperature readings
    temps = psutil.sensors_temperatures()

    # Check if 'coretemp' is in the readings
    if 'coretemp' in temps:
        for entry in temps['coretemp']:
            print(f"Label: {entry.label}, Current Temperature: {entry.current}°C")
    else:
        print("No temperature data available.")
    try:
        cpu_temperature = psutil.sensors_temperatures()['coretemp'][0].current  # For systems with temperature sensors
    except (KeyError, AttributeError):
        cpu_temperature = "Not available"  # If temperature info isn't available

    # Context to pass to template
    context = {
        'cpu_usage': cpu_usage,
        'cpu_temperature': cpu_temperature,
        'memory_total': memory_info.total / (1024 ** 3),  # Convert bytes to GB
        'memory_used': memory_info.used / (1024 ** 3),  # Convert bytes to GB
        'memory_free': memory_info.free / (1024 ** 3),  # Convert bytes to GB
        'disk_total': disk_info.total / (1024 ** 3),  # Convert bytes to GB
        'disk_used': disk_info.used / (1024 ** 3),  # Convert bytes to GB
        'disk_free': disk_info.free / (1024 ** 3),  # Convert bytes to GB
    }
    return render(request, 'system_info.html', context)


def system_info_api(request):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    try:
        cpu_temperature = psutil.sensors_temperatures()['coretemp'][0].current
    except (KeyError, AttributeError):
        cpu_temperature = "Not available"

    data = {
        'cpu_usage': cpu_usage,
        'cpu_temperature': cpu_temperature,
        'memory_total': memory_info.total / (1024 ** 3),  # Convert bytes to GB
        'memory_used': memory_info.used / (1024 ** 3),  # Convert bytes to GB
        'memory_free': memory_info.free / (1024 ** 3),  # Convert bytes to GB
        'disk_total': disk_info.total / (1024 ** 3),  # Convert bytes to GB
        'disk_used': disk_info.used / (1024 ** 3),  # Convert bytes to GB
        'disk_free': disk_info.free / (1024 ** 3),  # Convert bytes to GB
    }
    return JsonResponse(data)
