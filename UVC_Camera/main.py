#!/usr/bin/env python3

"""
  Name:    main.py
  Version: v1.0
  License: GPL
  Author:  Riviere
  Date:    27 May, 2022
  Description:
         This script demonstrates how to use the camera.py library.
"""
from camera import Camera
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows

if __name__=='__main__':
  cam=Camera(
    ID=0,
    RESOLUTION=(180,160),
    ERROR_TEXT='Disconnect!',
    TEXT_SIZE=0.4
  )
  while True:
    imshow('raw',cam.getFrame())
    if waitKey(33)==27:
      break

  cam.releaseCamera()
  destroyAllWindows()
