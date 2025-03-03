import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize picamera2
picam2 = Picamera2()

# Start the camera preview
picam2.start_preview()

# Configure the camera for video capture (video configuration for continuous frames)
picam2.configure(picam2.create_video_configuration())
picam2.set_controls({"AwbEnable": False})
# Start capturing frames
picam2.start()

# Main loop for capturing and displaying frames
while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Ensure the frame is in BGR format for OpenCV
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the frame in a window
    cv2.imshow('Camera Feed', frame_bgr)

    # Wait for key press and check if the Escape key (27) is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key
        print("Escape key pressed. Exiting...")
        break

# Release resources and close the OpenCV window
cv2.destroyAllWindows()
picam2.stop()
