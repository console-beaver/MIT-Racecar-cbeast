"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3B - Depth Camera Cone Parking
"""

########################################################################################
# Imports
########################################################################################

import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()
ORANGE = ((10, 100, 100), (20, 255, 255))
MIN_CONTOUR_AREA = 30

# Add any global variables here

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    global pastTerm
    global derivTerm
    pastTerm = 0
    derivTerm = 0
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Lab 3B - Depth Camera Cone Parking")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Park the car 30 cm away from the closest orange cone.
    # Use both color and depth information to handle cones of multiple sizes.
    # You may wish to copy some of your code from lab2b.py
    image = rc.camera.get_color_image()
    contours = rc_utils.find_contours(image,ORANGE[0],ORANGE[1])
    contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA) 
    if contour is not None:
        contour_center = rc_utils.get_contour_center(contour)
        rc_utils.draw_contour(image,contour)
        rc_utils.draw_circle(image,contour_center)
    else:
        contour_center = 0

    scan = rc.lidar.get_samples()
    __,coneDist = rc_utils.get_lidar_closest_point(scan, (-20,20))

    if contour is not None:
        global pastTerm
        global derivTerm
        angleTerm = contour_center[1] - rc.camera.get_width()/2
        speedTerm = coneDist - 50
        derivTerm = (speedTerm - pastTerm)/rc.get_delta_time() if speedTerm != pastTerm else derivTerm
        speedSign = speedTerm/abs(speedTerm) if speedTerm != 0 else 0

        print(str(speedTerm)+" and "+str(derivTerm))

        angle = angleTerm * (1/200) #angle P controller
        speed = speedTerm * (1/50) + derivTerm * (1/250) #speed P"D" controller

        angle = -1 if angle < -1 else angle
        angle = 1 if angle > 1 else angle
        speed = -1 if speed < -1 else speed
        speed = 1 if speed > 1 else speed
        #speed = 0 if abs(derivTerm) < 15 else speed 

    else:
        speed = 0
        angle = 0

    pastTerm = speedTerm
    rc.drive.set_speed_angle(speed,angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
