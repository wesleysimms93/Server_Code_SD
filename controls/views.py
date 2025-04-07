

# Create your views here.
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


#Were Pitcures are stored
media_dir = os.path.join(os.getcwd(), 'media/pictures')
#Global URL for the Camera Checked when the system requests the location 
Cam_URL = ""
#Should have this only run once
#Need to fix that. 
def testconnection():
    if(Cam_URL != ""):
        return Cam_URL
    Camera_URL = "http://192.168.8.3:5000"
    try:
        response = requests.get(Camera_URL+"/test_connection", timeout=5)
        if response.status_code == 200:
            print("Connection Over Ethernet")
            return Camera_URL
        else: 
            print("Don't Know what happend but you got this")
            return "http://192.168.8.3:5000"
    except requests.ConnectionError:
        print("Defalting to WIFI")
        Camera_URL = "http://192.168.137.135:5000"
        return Camera_URL

@login_required
def manual_control(request):
    Camera_URL = testconnection()
    return render(request, 'manual_control.html', {'Cam_url': Camera_URL+"/video_feed"})



@login_required
def download_from_external(request):
    Camera_URL = testconnection()
    image_url = Camera_URL+"/Raw_Capture"  # Replace with the actual URL of the image

    try:
        # Make a request to the external website
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Create an HttpResponse object with the fetched image content
            content_type = response.headers['Content-Type']
            image_data = response.content
            # Extract the file name from the URL (e.g., 'image.jpg')
            
            now = datetime.now().strftime("%m-%d_%H:%M:%S")

            #image_name = os.path.basename(image_url)
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
    





def generate_frames():
    Camera_URL = testconnection()
    # Replace 'YOUR_IP_CAMERA_URL' with your IP camera's RTSP or HTTP URL
    camera = cv2.VideoCapture(Camera_URL)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_stream(request):
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')