#!/usr/bin/env python3
# VITA, EPFL


##################
#IMPORTS
##################
import rospy
import matplotlib.pyplot as plt
import time
import glob
from datetime import datetime

import os
import sys

from tools import classes
import csv
import cv2
import numpy as np

now = datetime.now().strftime("%Y%m%d%H%M%S")
filename_data = "Stream_MR_" + str(now) + ".csv"
filename_video = "Stream_MR_" + str(now) + ".avi"
save_results = False

from perceptors import sot_perceptor, mot_perceptor
from detectors import yolov5_detector, pifpaf_detector
from trackers import mmtracking_sot
from utilities.utils import Utils



def img_sync(excess_img, current_img, socket, verbose):
    #to avoid an offset in the img transmission due to desynchronization of transmission
    if excess_img:
        current_img += excess_img
    current_img += socket.received_data
    # if verbose:
    #     print(f"img len before {len(current_img)}")
    while len(current_img) > socket.data_size:
        current_img=current_img[socket.data_size:]
    # if verbose:
    #     print(f"len after sync {len(current_img)}")
    #     print(f"socket {len(socket.received_data)}, size {socket.data_size}")
    return current_img

def check_img_sync(input_img, socket, verbose):
    if verbose:
        print("Image Transmission not synced !!")
    next_img=input_img[socket.data_size:]
    while len(next_img) > socket1.data_size:
        next_img=input_img[socket1.data_size:]
    if verbose:
        print(f"surplus {len(next_img)}")
    return next_img


def main():
    ###################################
    # Config from Launch File Arguments
    ####################################
    # Initialize ROS perception node
    rospy.init_node("perception")
    dt_perception = rospy.get_param("/dt_perception")
    rate = rospy.Rate(int(1/dt_perception))    
    PERCEPTION_FUNCTION = rospy.get_param("/PERCEPTION_FUNCTION")
    downscale = rospy.get_param("/downscale")
    detector_size=rospy.get_param("/detector_size")
    tracking_conf=rospy.get_param("/tracking_confidence")
    perception_vis=rospy.get_param("/visualization_activated")
    verbose=rospy.get_param("/verbose_percep")
    
    ###################################
    # Initialize Full detector
    ###################################
    # Initialize Detector Configuration
    # Set width, height and channel values for the received image --> Loomo image dimensions without downscale: 640x480x3

    # if PERCEPTION_FUNCTION == "Default":
    #     perceptor = classes.DetectorConfig(width = 80, height = 60, channels = 3, downscale = downscale,
    #                                             global_path = path_model,
    #                                             detector = detector.Detector(), load = True, type_input = "opencv")
    
    if PERCEPTION_FUNCTION =="Openpifpaf":
        # perceptor = classes.NewDetectorConfig(width = 640, height = 480, channels = 3, downscale = downscale,
        #                                         global_path = '',
        #                                         detector = pifpaf_detector.Detector_pifpaf(), load = False, type_input = "pil",
        #                                         save_video=save_results, filename_video=filename_video)
        perceptor = mot_perceptor.MotPerceptor(width = 640, height = 480, channels = 3, downscale = downscale,
                                                detector = pifpaf_detector.Detector_pifpaf, detector_size="default", 
                                                tracker=None, tracker_model=None, tracking_conf=None,
                                                type_input = "pil", verbose=False)


    elif PERCEPTION_FUNCTION =="Yolo":
        perceptor = classes.NewDetectorConfig(width = 640, height = 480, channels = 3, downscale = downscale,
                                                global_path = '',
                                                detector = yolo_detector.YoloDetector(), load = False, type_input = "opencv",
                                                save_video=save_results, filename_video=filename_video)
    
    elif PERCEPTION_FUNCTION =="Stark":
        perceptor = sot_perceptor.SotPerceptor(width = 640, height = 480, channels = 3, downscale = downscale,
                                                detector = yolov5_detector.Yolov5Detector, detector_size="default", 
                                                tracker=mmtracking_sot.SotaTracker, tracker_model="Stark", tracking_conf=tracking_conf,
                                                type_input = "opencv", verbose=False)


    #################################
    # Initialize socket connections
    #################################
    #socket connection with Loomo => socket1: Receiver = Loomo's Camera; socket5: Sender = Detection Bbox 
    ip_address = rospy.get_param("/ip_address")
    #try:
    socket1 = classes.SocketLoomo(8081, dt_perception, ip_address, perceptor.data_size)
    #except NameError:
        #detection_image=None
    socket5 = classes.SocketLoomo(8085, dt_perception, ip_address, packer=25*'f ')

    #socket connection NeuroRestore
    #ip_address_nicolo = rospy.get_param("/ip_address_nicolo")
    #socket6 = classes.SocketLoomo(8086, dt_perception, ip_address_nicolo, packer=13*'f ', sockettype="datagram")

    init = time.time()
    ##############################
    # Main Loop
    ###############################
    # Initialize perception transmission variables
    received_image = b''
    data_rcvd=False
    next_img=[]

    rospy.loginfo("Perception Node Ready")

    with open(filename_data, 'w') as f:
        writer = csv.DictWriter(f, dialect='excel', fieldnames=['time', 'lhx', 'lhy', 'rhx', 'rhy', 'lkx', 'lky', 'rkx', 'rky', 'lax', 'lay', 'rax', 'ray'])
        writer.writeheader()

        while not rospy.is_shutdown():
            #rospy.loginfo("Perception loop")
            start = time.time()
            ################################
            # Receive Image from the Loomo
            ################################
            socket1.receiver(True)
            received_image=img_sync(next_img, received_image, socket1, verbose)
            next_img=[]

            if len(received_image)==socket1.data_size:
                data_rcvd=True
                # Reset perception variables
                input_img=received_image
                received_image = b''
                #############################
                # Inference on Received Image
                #############################
                bbox_list, label_list, bboxes_legs, image = perceptor.forward(input_img)
                if verbose:
                    print("Perception: bbox list:", bbox_list)

                ############################
                # Bounding Boxes Processing and Formatting
                #############################
                bbox = tuple()
                bbox_visu=None
                #Here we have only 1 bbox at the end as we are in Sot configuration
                if bbox_list and np.asarray(bbox_list).ndim==1:
                    # Send bbox positions via socket to represent them in the Loomo
                    bbox_visu = bbox + (bbox_list[0], bbox_list[1], bbox_list[2], bbox_list[3], float(True))#float(label_list[i][0]))
                    #Scaling down bbox so that depth estimation is more precise
                    scale=0.3
                    bbox_list=Utils.bbox_scaling(bbox_list, scale)
                    #Loomo with Vita Testing App want the bbox in the following format: x_tl, y_tl, w, h
                    new_bbox=Utils.bbox_xcentycentwh_to_xtlytlwh(bbox_list)
                    bbox= bbox+(new_bbox[0], new_bbox[1], new_bbox[2], new_bbox[3], float(True))

                elif PERCEPTION_FUNCTION =="Openpifpaf":
                        for bbox_indiv in bbox_list:
                            bbox_visu = Utils.bbox_xtlytlwh_to_xcentycentwh(bbox_indiv)
                            bbox=bbox+(bbox_indiv[0], bbox_indiv[1], bbox_indiv[2], bbox_indiv[3], float(True))
                else:
                    bbox=bbox+(0.0, 0.0, 0.0, 0.0, float(False))            

                ###################################
                # Transmission to Loomo
                ###################################
                # Send bbox to the robot -> Camera tracking and motion controller algorithm

                #Tests with Hand coded bbox
                #bbox= (0.0, 0.0, 0.0, 0.0, 1.0) #trying to hand code 0 bbox to see if it's transmitted
                #transmitting fake bbox in the center
                # bbox_list=[160, 120, 50, 100]
                # x_tl= bbox_list[0] - bbox_list[2]/2
                # y_tl= bbox_list[1] - bbox_list[3]/2
                # w= bbox_list[2]
                # h= bbox_list[3]
                # bbox= (x_tl, y_tl, w, h, float(True))

                bbox = bbox + (0.0,)*(25-len(bbox)) #this line just adding 20 times 0.0 after bbox which is 4+ 1 (label)
                socket5.sender(bbox)

                ####################################
                # Keypoints Logging & Transmission #
                ####################################
                # pixel_legs = tuple()

                # for i in range(len(bboxes_legs)):
                #     # Send bbox positions via socket to represent them in the Loomo
                #     pixel_legs = pixel_legs + (bboxes_legs[i][0], bboxes_legs[i][1])

                # pixel_legs = tuple([time.time()-init]) + pixel_legs
                # pl = pixel_legs[:13]
                
                # if pl[1]!=0.0:
                #     # Send information to NeuroRestore Stimulation algorithm
                #     socket6.sender(pl)

                # if save_results:
                #     dict_legs = {'time': pl[0], 'lhx': pl[1], 'lhy': pl[2], 'rhx': pl[3], 'rhy': pl[4], 'lkx': pl[5], 'lky': pl[6], 'rkx': pl[7], 'rky': pl[8], 'lax': pl[9], 'lay': pl[10], 'rax': pl[11], 'ray': pl[12]}
                #     writer.writerow(dict_legs)

            #syncing Img transmission
            elif len(received_image) > socket1.data_size:
                next_img=check_img_sync(received_image, socket, verbose)
                received_image = b''

            # Calculate node computation time
            computation_time = time.time() - start

            if computation_time > dt_perception:
                rospy.logwarn("Perception computation time higher than node period by " + str(computation_time-dt_perception) + " seconds")

            if data_rcvd:
                data_rcvd=False
                rate.sleep()

    f.close()

if __name__ == "__main__":

    try:
        main()

    except rospy.ROSInterruptException:
        pass





            

            


