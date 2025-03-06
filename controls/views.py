

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


#Global URL for the Camera Checked when the system requests the location 
Camera_URL = "http://192.168.100.2:5000"

def printer_control(request):
    return render(request, 'wifi/3d_printer.html')

@login_required
def manual_control(request):
    return render(request, 'manual_control.html')



@login_required
def download_from_external(request):
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