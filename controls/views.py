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
#from picamera2 import Picamera2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
import subprocess


#Were Pitcures are stored
media_dir = os.path.join(os.getcwd(), 'media/pictures')
#Global URL for the Camera Checked when the system requests the location 
Cam_URL = ""
#Should have this only run once
#Need to fix that. 
def testconnection():
    global Cam_URL  # Ensure the global variable is used
    if Cam_URL:
        return Cam_URL  # Return the cached URL if available

    Camera_URL = "http://192.168.8.3:5000"
    try:
        response = requests.get(Camera_URL + "/test_connection", timeout=5)
        if response.status_code == 200:
            print("Connection Over Ethernet")
            Cam_URL = Camera_URL  # Cache the URL
            return Camera_URL
        else:
            print("Camera connection failed, using default URL")
            return "http://placeholder-url.com"  # Fallback URL
    except requests.ConnectionError:
        print("Defaulting to placeholder URL due to connection error")
        return "http://placeholder-url.com"  # Fallback URL

@login_required
def manual_control(request):
    Camera_URL = testconnection()
    if Camera_URL == "http://placeholder-url.com":
        print("Warning: Camera connection failed. Using placeholder URL.")
    return render(request, 'manual_control.html', {'Cam_url': Camera_URL + "/video_feed"})



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
            
            now = datetime.now().strftime("%m_%d_%H_%M_%S")

            #image_name = os.path.basename(image_url)
            image_path = os.path.join(media_dir,"Manual_Control", now + "_pic.jpg")

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
    if Camera_URL == "http://placeholder-url.com":
        print("Warning: Camera feed unavailable. Returning placeholder frames.")
        while True:
            # Generate a placeholder frame (e.g., a blank image)
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Black image
            _, buffer = cv2.imencode('.jpg', blank_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1)  # Simulate a frame rate
    else:
        camera = cv2.VideoCapture(Camera_URL)
        while True:
            success, frame = camera.read()
            if not success:
                print("Error: Unable to read frame from camera.")
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

def execute_cool_script(request, action):
    try:
        # Call the cool.py script with the action as an argument
        subprocess.run(['python', 'cool.py', action], check=True)
        return JsonResponse({'status': 'success', 'message': f'Executed action: {action}'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})