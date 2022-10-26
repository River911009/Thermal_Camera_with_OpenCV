#!/usr/bin/env python3

"""
  Name:    main.py
  Version: v1.0
  License: GPL
  Author:  Riviere
  Data:    26 Oct, 2022
  Description:
         This script demonstrates how to get temperature array from GTM016A module
    via CDC protocol.

Raises:
  SystemError raised if the serial port isn't available.
"""
import serial
from time import sleep

# GTM016A port name
GTM016A_PORT='xxxx' # change 'xxxx' to your serial port name.
# GTM016A get device ID command
GET_DEVICE_ID=[0]
# GTM016A get temperature image command
GET_TEMP_IMAGE=[83]
# receive buffer
receive_buffer=[0]*514
# the 16 x 16 temperature array in degree celsius
temperature_array=[[0]*16]*16


# prepare serial connection handler
port=serial.Serial(
  port=GTM016A_PORT,
  baudrate=115200,
  bytesize=serial.EIGHTBITS,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  timeout=10
)

# open connection
if port.isOpen():
  pass
else:
  raise SystemError("Serial port not found!")


"""Get Device ID
  write:  0x00
  read:   0x11(17)
"""
port.flushInput()
port.write(GET_DEVICE_ID)
sleep(0.001)
if port.in_waiting>=1:
  receive_buffer[0]=port.read(1)
# decode data
GTM016A_id=list(receive_buffer[0])[0]
print("Get Device ID, return: %d\n"%(GTM016A_id))


"""Get Temp Image and PCB Temp
  write:  0x53
  read:   514 bytes array
  decode: temperature=temp[0]+temp[1]*256
"""
port.flushInput()
port.write(GET_TEMP_IMAGE)
sleep(0.001)
if port.in_waiting>=514:
  receive_buffer=port.read(514)
# decode and print pcb temperature and image
pcb_temperature=(receive_buffer[512]+receive_buffer[513]*256)/100
print("PCB Temp: %.2f\n"%(pcb_temperature))
print("Temp Image:")
for y in range(16):
  for x in range(16):
    temperature_array[y][x]=(receive_buffer[(y*16+x)*2]+receive_buffer[(y*16+x)*2+1]*256)/100
    print('%5.2f'%(temperature_array[y][x]),end=' ')
  print('')


# close connection
port.close()
