# !/usr/bin/env python3

"""
  Name:    camera.py
  Version: v1.0
  License: GPL
  Author:  Riviere
  Date:    6 May, 2022
  Description:
         This library is built to easily get raw data array from 
    USB Video Class camera by opencv with automatic handle connection.
"""
from cv2 import VideoCapture
from cv2 import CAP_MSMF
from cv2 import CAP_PROP_FRAME_HEIGHT
from cv2 import CAP_PROP_FRAME_WIDTH
from cv2 import CAP_PROP_CONVERT_RGB
from cv2 import CAP_PROP_MODE
from cv2 import putText
from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import LINE_AA
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows

from numpy import zeros
from numpy import uint8
from numpy import reshape

from time import sleep

# VideoCapture controller
class Camera:
  """
   Create videocapture with camera connect detect
    parameters:
      [ID]          camera ID
      [RESOLUTION]  final 2D image shape
      [ERROR_TEXT]  message when camera disconnect
      [TEXT_SIZE]   size of the message

    1. openCamera()
    2. releaseCamera()
    3. getFrameFail()
      return black screen with error text
    4. getFrame()
      return reshaped 2D image if capture success
      or release camera when capture fail
  """
  def __init__(self,ID,RESOLUTION='',ERROR_TEXT='',TEXT_SIZE=''):
    # camera default configuration
    self.CAMERA_ID =ID
    self.RESOLUTION=RESOLUTION
    self.ERROR_TEXT=ERROR_TEXT
    self.TEXT_SIZE=TEXT_SIZE
    self.TEXT_POSITION=(20,60)
    self.REOPEN_TIME=0.1
    self.openCamera()

  def openCamera(self):
    # open live camera
    self.camera=VideoCapture(
      self.CAMERA_ID,
      CAP_MSMF
    )
    if self.camera.isOpened():
      # get camera resolution
      if self.RESOLUTION=='':
        self.RESOLUTION=(
          int(self.camera.get(CAP_PROP_FRAME_HEIGHT)*1.5),
          int(self.camera.get(CAP_PROP_FRAME_WIDTH))
        )
        if self.RESOLUTION==(0,0):
          self.RESOLUTION=(1,1)
      # set camera to YUV mode(RAW data 1.5 times lt resolution)
      self.camera.set(CAP_PROP_CONVERT_RGB,0)
      self.camera.set(CAP_PROP_MODE,3)

  def releaseCamera(self):
    self.camera.release()

  def getFrameFail(self):
    img=zeros(shape=self.RESOLUTION,dtype=uint8)
    if self.ERROR_TEXT!='':
      putText(
        img=img,
        text=self.ERROR_TEXT,
        org=self.TEXT_POSITION,
        fontFace=FONT_HERSHEY_SIMPLEX,
        fontScale=self.TEXT_SIZE,
        color=255,
        thickness=1,
        lineType=LINE_AA
      )
    return(img)

  def getFrame(self):
    ret,img=self.camera.read()
    if ret:
      img=reshape(img,self.RESOLUTION)
    else:
      img=self.getFrameFail()
      self.releaseCamera()
      sleep(self.REOPEN_TIME)
      self.openCamera()
    return(img)

##################################################
# Test the library
##################################################
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
