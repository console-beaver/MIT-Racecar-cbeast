"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3C - Depth Camera Wall Parking
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

# Add any global variables here

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    global pastTerm
    pastTerm = 0
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Lab 3C - Depth Camera Wall Parking")


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO: Park the car 20 cm away from the closest wall with the car directly facing
    # the wall

    global pastTerm
    scan = np.array(rc.lidar.get_samples())
    scan.setflags(write=1)
    scan[scan < 0.1] = 9999

    minDist = min(scan)
    minIndex = np.where(scan==min(scan))[0][0]
    minAngle = minIndex/2 #0<=angle<=360
    minAngle -= 360 if minAngle > 180 else 0 #-180<=angle<=180
    
    angleTerm = minAngle - 0
    speedTerm = minDist - 41
    derivTerm = (speedTerm - pastTerm)/rc.get_delta_time()

    angle = angleTerm/20 #angle P controller
    speed = (speedTerm/150 + derivTerm/150) #speed PD controller

    angle = -1 if angle < -1 else angle
    angle = 1 if angle > 1 else angle
    speed = -1 if speed < -1 else speed
    speed = 1 if speed > 1 else speed

    pastTerm = speedTerm

    rc.drive.set_speed_angle(speed,angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
