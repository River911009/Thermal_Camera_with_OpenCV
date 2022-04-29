# !/usr/bin/env python3

"""
  Name:    main_basic_demo.py
  Version: v1.0
  License: GPL
  Author:  Riviere
  Date:    28 April, 2022
  Description:
         This script is built to demonstrate the GTM640/GTM320/GTM160 thermal camera
    which using USB Video Class protocol.
"""

# Dependency import
import cv2

# Using opencv to open connection
try:
  cap=cv2.VideoCapture(0)
except:
  print("Can not connect to camera.")
  exit(1)

# Test connection
if not cap.isOpened():
  print("Camera is not connected.")
  exit(1)

# Prepare display loop
print("Press ESC to exit the app...")

while True:
  # Get image from camera
  ret,img=cap.read()

  # Show image if capture success
  if ret:
    cv2.imshow("Thermal Camera Viewer",img)
  
  # Delay 33mS(~30fps) and detect ESC button press
  if cv2.waitKey(33)==27:
    break

# Release resources after exit the display loop
cap.release()
cv2.destroyAllWindows()
