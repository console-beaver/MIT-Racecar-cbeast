"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 3A - Depth Camera Safety Stop
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
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(
        ">> Lab 3A - Depth Camera Safety Stop\n"
        "\n"
        "Controls:\n"
        "   Right trigger = accelerate forward\n"
        "   Right bumper = override safety stop\n"
        "   Left trigger = accelerate backward\n"
        "   Left joystick = turn front wheels\n"
        "   A button = print current speed and angle\n"
        "   B button = print the distance at the center of the depth image"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # Use the triggers to control the car's speed
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = rt - lt

    # Calculate the distance of the object directly in front of the car
    depth_image = rc.camera.get_depth_image()
    center_distance = rc_utils.get_depth_image_center_distance(depth_image)

    # TODO (warmup): Prevent forward movement if the car is about to hit something.
    crop_mid = depth_image[:int(2*rc.camera.get_height()/5),-30+int(rc.camera.get_width()/2):30+int(rc.camera.get_width()/2)]
    crop_mid = (crop_mid - 0.01) % 10000
    blur_mid = cv.GaussianBlur(crop_mid,(5,5),cv.BORDER_DEFAULT)
    closestMid,__,__,__ = cv.minMaxLoc(blur_mid)
    safeSpeed = 0 if closestMid < 90 and speed > 0 else speed

    print("closestMid: "+str(closestMid))
    #print(closestMid)

    # Allow the user to override safety stop by holding the right bumper.
    speed = safeSpeed if rc.controller.is_down(rc.controller.Button.RB) == False else speed

    # Use the left joystick to control the angle of the front wheels
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the depth image center distance when the B button is held down
    if rc.controller.is_down(rc.controller.Button.B):
        print("Center distance:", center_distance)

    # Display the current depth image
    #rc.display.show_depth_image(depth_image)

    # TODO (stretch goal): Prevent forward movement if the car is about to drive off a
    # ledge.  ONLY TEST THIS IN THE SIMULATION, DO NOT TEST THIS WITH A REAL CAR.
    crop_bottom = depth_image[int(19*rc.camera.get_height()/20):rc.camera.get_height(),-30+int(rc.camera.get_width()/2):30+int(rc.camera.get_width()/2)]
    crop_bottom = (crop_bottom - 0.1)%10000
    blur_bottom = cv.GaussianBlur(crop_bottom,(5,5),cv.BORDER_DEFAULT)
    __,farthestBottom,__,__ = cv.minMaxLoc(blur_bottom)

    safeSpeed = 0 if farthestBottom > 65 and speed > 0 else speed

    speed = safeSpeed if rc.controller.is_down(rc.controller.Button.RB) == False else speed

    print("farthestBottom: "+str(farthestBottom))


    # TODO (stretch goal): Tune safety stop so that the car is still able to drive up
    # and down gentle ramps.
    # Hint: You may need to check distance at multiple points.

    #I alraedy did this, look at the two uses of safetySpeed
    rc.drive.set_speed_angle(speed, angle)

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
