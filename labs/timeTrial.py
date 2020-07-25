import sys
import cv2 as cv
import numpy as np

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils


rc = racecar_core.create_racecar()
BLUE =  ((90,50,50),(100,255,255))
GREEN = ((35,50,50),( 70,255,255))
RED =   (( 0,50,50),( 10,255,255))
CROP_FLOOR = ((360,0),(rc.camera.get_height(),rc.camera.get_wdith()))
MIN_CONTOUR_AREA = 30

def start():
    rc.drive.stop()

def update():
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)

    depth_image = rc.camera.get_depth_image()
    center_distance = rc_utils.get_depth_image_center_distance(depth_image)

    angle = followLine()
    forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    backwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    speed = forwardSpeed - backwardSpeed
    #angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    rc.drive.set_speed_angle(speed,angle)

def followLine():
    cCenter,cArea = updateContour(RED,GREEN,BLUE)
    if cCenter is not None:
        errorTerm = cCenter[1]-320
        angle = errorTerm/320
    else:
        angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    return angle

def updateContour(color_priority):
    image = rc.camera.get_color_image()
    if image is None:
        contour_center = None
        contour_area = 0
    else:
        image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])
        for color in color_priority:
            contours = rc_utils.find_contours(image,color[0],color[1])
            if len(contours) > 0:
                break
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
        if contour is not None:
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)
            #rc_utils.draw_contour(image,contour)
            #rc_utils.draw_circle(image,contour_center)
        else:
            contour_center = None
            contour_area = 0
        return contour_center,contour_area

def update_slow():
    pass #NOTHING TO DO HERE

if __name__ == "__main__":
    rc.set_start_update(start,update,update_slow)
    rc.go()
