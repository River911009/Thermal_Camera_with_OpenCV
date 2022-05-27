# Thermal_Camera_SDK

This is a demonstration code for USB thermal camera built with OpenCV on Python. Based on GoalTop camera module.

# File Description

|  Name   | Recommand Device | Description |
|---------|------------------|-------------|
| License |  | This SDK developed with GPL license, any change or fork have to follow GPL rule. |
| HID_Module/* | GTM016A |  |
| HID_Module/* | GTM016A |  |
| UVC_Camera/main.py | GTM160, GTM640 | This script is a basic demonstration using __camera.py__ library. |
| UVC_Camera/camera.py | GTM160, GTM640 | Camera handler library which can receive raw uint8 data array without compressed. |
| UVC_Camera/demo_commands.py | GTM160, GTM640 | This script shows how to use some basic commands on CLI to handle camera. |

# Environment Require

Tested Platform:
* Windows 10: 21H2
* Ubuntu 20.04: Kernel 5.13

Dependencies:
* python : 3.8
* opencv-python: 4.5.4

----

# To be modify on next push
[ ] (camera.py).openCamera(): add auto detect os platform to set VideoCapture param with CAP_MSMF or other.