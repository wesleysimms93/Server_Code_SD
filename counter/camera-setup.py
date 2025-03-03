import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize picamera2
picam2 = Picamera2()

# Start the camera preview
#picam2.start_preview()


# Configure the camera for video capture (video configuration for continuous frames)
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.set_controls({"AwbEnable": False, "FrameRate": 15})
#picam2.set_controls({"LensMode": 0})  # Typically 0 for IR-CUT off, 1 for IR-CUT on, depending on camera
# Start capturing frames
test = True
picam2.start()
test2 = 0
# Main loop for capturing and displaying frames
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 13:
        test = True
        picam2.start()
    if test:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        #print(picam2.camera_status())  # Print camera status for debugging
        # Ensure the frame is in BGR format for OpenCV
        #frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Display the frame in a window
        cv2.imshow('Camera Feed', frame)
    # Wait for key press and check if the Escape key (27) is pressed
    if key == 27:  # Escape key
        print("Escape key pressed. Exiting...")
        test = False
        picam2.stop()
            
    
        

# Release resources and close the OpenCV window
cv2.destroyAllWindows()
picam2.stop()
