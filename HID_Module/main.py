#!/usr/bin/env python3

"""
  Name:    main.py
  Version: v1.0
  License: GPL
  Author:  Riviere
  Data:    3 Aug, 2022
  Description:
         This script demonstrates how to get temperature array from GTM016A module
    via PL23C3 HID to I2C bridge.

Raises:
  SystemError:
    SystemError raised if the PL23C3 bridge isn't available.
"""
from os import *
from ctypes import *
from struct import pack


# GTM016A_ADDRESS is the I2C device address of GTM016A, see page 1 of GTM016A_Module.pdf
GTM016A_ADDRESS=48
# DEVICE_VID is the vid of Prolific PL23C3
DEVICE_VID=c_uint16(1659)
# prepare read/write buffer
wData=create_string_buffer(1)
rData=create_string_buffer(512)
rLength=c_uint32(0)
# the 16 x 16 temperature array in degree celsius
temperature_array=[[0]*16]*16

# load corresponding DLL depends on cpu architecture
if environ["PROCESSOR_ARCHITECTURE"].endswith('64'):
  module=CDLL("./HidDeviceSdk_x64.dll")
else:
  module=CDLL("./HidDeviceSda_x86.dll")

# prepare I2C connection handler
handle=c_void_p()
# find bridge board by vid
device_count=c_uint32(0)
module.EnumDeviceByVid(byref(device_count),DEVICE_VID)


# open connection, set I2C device address and frequency if bridge board is available
if device_count.value>0:
  module.OpenDeviceHandle(0,byref(handle))
  module.SetI2CDeviceAddress(handle,GTM016A_ADDRESS)
  # the frequency can be changed from 94khz to 6Mhz
  # I2C Frequency(khz)=24000000/240=100khz
  # please see the example code of Prolific PL23C3 SDK
  module.SetI2CFrequency(handle,24)
# raise error if bridge board isn't available
else:
  raise SystemError("Module not found!")


"""Get Device ID
  write:  0x00
  read:   0x11(17)
"""
rdata_size=1
reg_address=0
wData.raw=pack('B',reg_address)
module.I2CWriteRead(handle,byref(wData),1,byref(rData),rdata_size,byref(rLength),100)
# decode data
temp=list(rData.raw)[:rdata_size]
GTM016A_id=temp[0]
print("Get Device ID, return: %d\n"%(GTM016A_id))


"""Get PCB Temp
  write:  0x14
  read:   2 bytes array
  decode: temperature=temp[0]*256+temp[1]
"""
rdata_size=2
reg_address=20
wData.raw=pack('B',reg_address)
module.I2CWriteRead(handle,byref(wData),1,byref(rData),rdata_size,byref(rLength),100)
# decode data
temp=list(rData.raw)[:rdata_size]
pcb_temperature=(temp[0]*256+temp[1])/100
print("Get PCB Temp, return: %.2f\n"%(pcb_temperature))


"""Get Temp Image
  write:  0x64
  read:   512 bytes array
  decode: temperature=temp[0]*256+temp[1]
"""
rdata_size=512
reg_address=100
wData.raw=pack('B',reg_address)
module.I2CWriteRead(handle,byref(wData),1,byref(rData),rdata_size,byref(rLength),100)
# decode and print temperature array in 2D
temp=list(rData.raw)[:rdata_size]
print("Get Temp Image, return:")
for y in range(16):
  for x in range(16):
    temperature_array[y][x]=(temp[(y*16+x)*2]*256+temp[(y*16+x)*2+1])/100
    print('%5.2f'%(temperature_array[y][x]),end=' ')
  print('')


# close connection
module.CloseDeviceHandle(handle)
