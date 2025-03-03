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
from django.core.exceptions import SuspiciousOperation

# Global variable to hold the count (for demonstration purposes only)
count = 0
# Global variable to control the camera feed thread
camera_thread = None
feed_active = False
picam2 = None
test = 0;
media_dir = os.path.join(os.getcwd(), 'media/pictures')

@login_required
def index(request):
    return render(request, 'counter/index.html', {'count': count})

@login_required
def printer_control(request):
    return render(request, 'counter/3d_printer.html')

@login_required
def increment(request):
    global count
    count += 1
    return JsonResponse({'count': count})

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
    return render(request, 'counter/system_info.html', context)



def gen_camera_feed():
    global feed_active, picam2, test
    if test == 0:
        print(feed_active)
        test += 1
        feed_active = False
    #picam2 = None
    # Initialize Picamera2 only once
    if picam2 is None:
        picam2 = Picamera2()
        
        # Start the camera preview
        picam2.start_preview()

        # Configure the camera for video capture (video configuration for continuous frames)
        picam2.configure(picam2.create_video_configuration())
        picam2.set_controls({"AwbEnable": False})
        # Start capturing frames
    if feed_active:
        picam2.start()
    
    try:
        while feed_active:
            frame = picam2.capture_array()

            # Ensure the frame is in BGR format for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # Encode the frame as JPEG (color format)
            _, jpeg = cv2.imencode('.jpg', frame_bgr)

            # Convert to bytes for streaming
            frame_bytes = jpeg.tobytes()

            # Yield the frame as a multipart response
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        
    finally:
        print("done")
        picam2.stop()  # Ensure the camera is stopped when done
        print(picam2)
            
            
def video_feed(request):
    global feed_active , picam2
    if not feed_active:
        feed_active = True  # Start the feed
        return StreamingHttpResponse(gen_camera_feed(), content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return JsonResponse({"status": "already_active"})

def stop_feed(request):
    global feed_active , picam2
    feed_active = False  # Stop the feed
    picam2.stop()  # Ensure the camera is stopped when done
    return JsonResponse({"status": "stopped"})

#def start_feed:
def download_from_external(request):
    image_url = "http://192.168.137.135:5000/Raw_Capture"  # Replace with the actual URL of the image

    try:
        # Make a request to the external website
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create an HttpResponse object with the fetched image content
            content_type = response.headers['Content-Type']
            image_data = response.content
            # Extract the file name from the URL (e.g., 'image.jpg')
            
            now = datetime.now().strftime("%m-%d %H:%M:%S")

            image_name = os.path.basename(image_url)
            image_path = os.path.join(media_dir, now + "_pic.jpg")

            # Save the image to the Media folder
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)

            # Return the image as an HTTP response with the appropriate content type
            return HttpResponse(image_data, content_type=content_type)

        else:
            raise SuspiciousOperation("Failed to fetch the image from the external website.")

    except requests.exceptions.RequestException as e:
        raise SuspiciousOperation(f"An error occurred while fetching the image: {e}")


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
