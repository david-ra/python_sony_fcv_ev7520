import re
import binascii
import numpy as np
from dataclasses import dataclass, field
from serial.tools import list_ports, list_ports_common
import cv2
import serial
import time
from typing import List

# Configure logging
import logging as logger
logger.basicConfig(
    level=logger.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s')  # Define the log message format

# GLOBAL FLAG FOR STREAMING STATE - ON/OFF
continue_streaming = True

def stop_streaming(signal, frame):
    global continue_streaming
    logger.info("Stopping streamming service...")
    continue_streaming = False

@dataclass
class SonyCamera():
    vid:str
    pid:str
    streaming_channel:int = field(default=1)
    command_channel:int = field(default=2)
    camera_id:int = field(default=0)
    port: str = field(init=False)
    info: list_ports_common.ListPortInfo = field(init=False)
    conn: serial.Serial = field(init=False)
    optical_zoom_positions:List[str] = field(init=False)

    def __post_init__(self):

        self.optical_zoom_positions = [
            "0000" if a == 0 else f"{'0' * max(0, 4 - len(hex(a-1).split('x')[1]))}{hex(a-1).split('x')[1]}"
            for a in range(0, 16386, 565)
            ]

        devices = list_ports.comports()
        for index, device in enumerate(devices):
            if (device.vid != None or device.pid != None):
                vid_pid = f"{'{:04X}'.format(device.vid)}:{'{:04X}'.format(device.pid)}" 
                if (vid_pid.lower() == f"{self.vid}:{self.pid}".lower()):
                    self.info = device
                    self.port = device.device
                    self.conn = serial.Serial(self.port, baudrate=9600, timeout=2)
                    self.camera_id = 0
                    self.stream = cv2.VideoCapture(self.camera_id)
                else:
                    self.info = None
                    self.port = None
                    self.port = None
                    self.stream = None
    


    def open(self):
        """Opens serial port.

        :param serial_port: Serial port to modify.
        :return: True if successful, False if not.
        :rtype: bool
        """
        if not self.conn.isOpen():
            self.conn.open()
            return True
        else:
            print ("Error opening serial port: Already open.")
            return False
    
    def close(self):
        """Closes current serial port.

        :param serial_port: Serial port to modify.
        :return: True if successful, False if not.
        :rtype: bool
        """
        if self.conn.isOpen():
            self.conn.close()
            return True
        else:
            print ("Error closing serial port: Already closed.")
            return False
    
    def initLens(self):
        command  = f"8{self.command_channel}01041901FF"
        response = self.sendCommand(command=command)
        print(response)
        return response
    
    def resetCamera(self):
        command  = f"8{self.command_channel}01041903FF"
        response = self.sendCommand(command=command)
        print(response)
        return response

    def on(self):
        command  = f"8{self.streaming_channel}01040002FF"
        response = self.sendCommand(command=command)
        print(response)
        return response
    
    def off(self):
        command  = f"8{self.streaming_channel}01040003FF"
        response = self.sendCommand(command=command)
        print(response)
        return response


    def zoom(self, zoom_position, x=1):
        positions = self.optical_zoom_positions[zoom_position-1]
        p, q, r, s = (position for position in positions)
        command = f"8{x}0104470{p}0{q}0{r}0{s}FF"
        response = self.sendCommand(command=command)
        return response
    


    def sendCommand(self, command):
        try:
            # Send the VISCA command
            self.conn.write(binascii.unhexlify(command))
            # Wait for a short time (adjust as needed)
            time.sleep(0.1)
            # Read the response
            response = self.conn.read(self.conn.in_waiting)
            print("Response:", response)
            return response
        except Exception as e:
            print(f"Error: {e}")

    def home(self):
        """Moves camera to home position.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.command('81010604FF') 
