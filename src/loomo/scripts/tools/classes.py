#!/usr/bin/env python3
# VITA, EPFL
import sys
import cv2
import socket
import numpy as np
import struct
import select
from PIL import Image
import rospy


class SocketLoomo:
    # Initialize socket connection
    def __init__(self, port, dt, host, data_size = 0, packer = 25*'f ', unpacker = 10*'f '):
        self.data_size = data_size
        self.max_waiting_time = dt/10
        self.received_data = []
        self.received_ok = False
        self.received_data_unpacked = []

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error:
            rospy.logerr('Failed to create socket')
            sys.exit()

        try:
            remote_ip = socket.gethostbyname(host)

        except socket.gaierror:
            rospy.logerr('Hostname could not be resolved. Exiting')
            sys.exit()

        rospy.loginfo('# Connecting to server, ' + host + ' (' + str(port) + ')')
        
        # Connect to IP address and port
        self.s.connect((remote_ip , port))
        # Create the packer
        self.packer = struct.Struct(packer)
        # Create the unpacker
        self.unpacker = struct.Struct(unpacker)

    # Receive data from the Loomo
    def receiver(self, is_image = False):

        if is_image:
            self.received_data = b''

        self.s.setblocking(0)
        # Set a timout value
        ready = select.select([self.s], [], [], self.max_waiting_time)
        self.received_ok = False
        # If data received before timeout value
        if ready[0]:
            self.received_ok = True

            if not is_image:
                self.received_data = self.s.recv(self.unpacker.size)
                # Unpack data converting it from bytes to floats
                self.received_data_unpacked = self.unpacker.unpack(self.received_data)

            else:
                self.received_data = self.s.recv(self.data_size)

    # Send data to the Loomo
    def sender(self, values):
        # Pack data from floats to bytes
        packed_data = self.packer.pack(*values)

        self.s.send(packed_data)


class DetectorConfig:
    # Initialize detector and its main properties
    def __init__(self, width, height, channels, downscale, global_path='', detector='', load=True, type_input="opencv"):
        # Detector expected input image dimensions
        self.width = int(width)
        self.height = int(height)
        self.downscale = downscale

        if self.downscale == 1:
            self.scale_necessary = False

        else:
            self.scale_necessary = True

        # Image received size data.
        self.data_size = int(width * height * channels/downscale)
        self.global_path = global_path
        self.detector = detector
        self.type_input = type_input

        if load:
            self.detector.load(global_path)

    def detect(self, received_image):
        # Adapt image to detector requirements
        pil_image = Image.frombytes('RGB', (80,60), received_image)

        if self.scale_necessary:
            maxsize = (self.width, self.height)
            pil_image = pil_image.resize(maxsize, Image.ANTIALIAS)

        opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        opencvImage = cv2.cvtColor(opencvImage,cv2.COLOR_BGR2RGB)
        #cv2.imshow('Test window',opencvImage)
        #cv2.waitKey(1)

        if self.type_input == "opencv":
            image = opencvImage
        
        elif self.type_input == "pil":
            image = pil_image

        bbox_list, bbox_label = self.detector.forward(image, self.downscale)

        return bbox_list, bbox_label


class MobileRobot:

    def __init__(self, wheel_base, v_max):
        self.wheel_base = wheel_base
        self.v_max = v_max
        self.w_max = 0.25

