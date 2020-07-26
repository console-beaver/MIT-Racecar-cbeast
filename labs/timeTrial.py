import sys
import cv2 as cv
import numpy as np
from nptyping import NDArray
from typing import Any,Tuple,List,Optional

sys.path.insert(0, "../library")
import racecar_core
import racecar_utils as rc_utils


rc = racecar_core.create_racecar()
BLUE =  (( 90,200, 50),(110,255,255))
GREEN = (( 35, 50, 50),( 70,255,255))
RED =   ((  0, 50, 50),( 10,255,255))
ORANGE =(( 11, 50, 50),( 20,255,255))
PURPLE =((130,200,200),(150,255,255))
SIDE_BLINDS = 0
CROP_FLOOR = ((300,SIDE_BLINDS),(rc.camera.get_height(),rc.camera.get_width()-SIDE_BLINDS))
MIN_CONTOUR_AREA = 30
STAGE = 0
FAST_COLOR = None

def start():
    rc.drive.stop()
    setLinePriority()

def update():
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    depth_image = rc.camera.get_depth_image()
    center_distance = rc_utils.get_depth_image_center_distance(depth_image)
    global STAGE
    if STAGE == 0:
        image = rc.camera.get_color_image()
        forwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
        backwardSpeed = rc.controller.get_trigger(rc.controller.Trigger.LEFT) 
        speed = forwardSpeed - backwardSpeed
        angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
        corners, ids = get_ar_markers(image)
        if ids is not None and 1 in ids:
            print("go fast!")
            STAGE = 2
        #if ids is not None and 199 in ids:
            #print("turn!")
    elif STAGE == 1:
        angle = followLine(COLOR_PRIORITY)
        speed = 1
    elif STAGE == 2:
        rc.set_max_speed = 3.0
        findOrangeOrPurpleAngle()
        speed = 0.1 #max possible
        angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    rc.drive.set_speed_angle(speed,angle)

def findOrangeOrPurpleAngle():
    global FAST_COLOR
    contour = None
    cCenter = None
    image = rc.camera.get_color_image()
    corners, ids = get_ar_markers(image)

    if True:
        for array in corners:
            ySum = 0
            xSum = 0
            for coordinates in array[0]:
                x,y = coordinates
                cv.circle(image,(x,y),2,(0,255,255),2)
                ySum+=y
                xSum+=x
            centerY=int(ySum/4)
            centerX=int(xSum/4)
            cv.circle(image,(centerX,centerY),4,(255,255,0),2)
            dispX=array[0][0][0]-array[0][1][0] if abs(array[0][0][0]-array[0][1][0])> 10 else array[0][0][0]-array[0][2][0]-5

            image_HSV = cv.cvtColor(image,cv.COLOR_BGR2HSV)
            if centerY > rc.camera.get_height():
                centerY-=1
            if centerX+0.85*abs(dispX) < rc.camera.get_width():
                print(centerX-int(abs(0.85*dispX)))
                color = image[centerX-int(abs(0.85*dispX)),centerY:]
                cv.circle(image,(centerX-int(abs(0.85*dispX)),centerY),4,(0,0,0),2)
            else:
                print(centerX-int(abs(0.85*dispX)))
                color = image[centerX+int(abs(0.85*dispX)),centerY,:]
                cv.circle(image,(centerX+int(abs(0.85*dispX)),centerY),4,(0,0,0),2)
            print("-----")
            print(color[0][0])
            print(PURPLE[0][0])
            print(PURPLE[1][0])
            print(ORANGE[0][0])
            print(ORANGE[1][0])
            print("----------")
            print(color)
            if color[0][0] > PURPLE[0][0] and color[0][0] < PURPLE[1][0]:
                FAST_COLOR = PURPLE
                print("purple")
            elif color[0][0] > ORANGE[0][0] and color[0][0] < ORANGE[1][0]:
                FAST_COLOR = ORANGE
                print("orange")
    if FAST_COLOR != None:
        #print(FAST_COLOR)
        pass
    rc.display.show_color_image(image)

#    if FAST_COLOR is not None:
#        image_cropped = rc_utils.crop(image,CROP_FLOOR[0],CROP_FLOOR[1])
#        contours = rc_utils.find_contours(image_cropped,FAST_COLOR[0],FAST_COLOR[1])
#        if contours is None:
#            contour = None
#        fastX = 0
#        for contour in contours:
#            if rc_utils.get_contour_center(contour) is not None:
#                if cv.contourArea(contour) > MIN_CONTOUR_AREA:
#                    print(cv.contourArea(contour))
#                    _,cCenter = rc_utils.get_contour_center(contour)
#                    fastX+=cCenter
#    if image is not None and FAST_COLOR is not None and contours is not None:
#        cCenter/=len(contours)
#        errorTerm = cCenter-320
#        angle = errorTerm/320
#    else:
#        angle = 0
#    return angle/2

def setLinePriority():
    global COLOR_PRIORITY
    COLOR_PRIORITY = []
    image = rc.camera.get_color_image()
    corners, ids = get_ar_markers(image)
    starterColors = [RED,GREEN,BLUE]
    itsThisOneChief = False
    for array in corners:
        ySum = 0
        xSum = 0
        for coordinates in array[0]:
            y,x = coordinates
            ySum+=y
            xSum+=x
        centerY = int(ySum/4)
        centerX = int(xSum/4)
        #cv.circle(image,tuple(map(int,array[0][0])),1,(255,255,0),4)
        #cv.circle(image,tuple(map(int,array[0][1])),1,(255,255,0),4)
        #cv.circle(image,tuple(map(int,array[0][2])),1,(255,255,0),4)
        #cv.circle(image,tuple(map(int,array[0][3])),1,(255,255,0),4)
        #cv.circle(image,(centerY,centerX),1,(0,255,255),4)
        displacementY = array[0][0][0] - array[0][1][0] if abs(array[0][0][0] - array[0][1][0]) > 30 else array[0][0][0] - array[0][2][0]
        if centerY+abs(displacementY) > rc.camera.get_height():
            color = convertBGRtoHSV(image[centerX,centerY-int(0.85*abs(displacementY)),:])
            cv.circle(image,(centerY-int(0.85*abs(displacementY)),centerX),5,(0,0,0),3)
        else:
            color = convertBGRtoHSV(image[centerX,centerY+int(0.85*abs(displacementY)),:])
            cv.circle(image,(centerY+int(0.85*abs(displacementY)),centerX),5,(0,0,0),3)
        if centerY < rc.camera.get_width()/2:
            itsThisOneChief = True
        if color[0] > 140 and color[0] < 170:
            starterColors.remove(GREEN)
            if itsThisOneChief:
                firstColor = GREEN
                itsThisOneChief = False
            else:
                lastColor = GREEN
        elif color[0] > 170 and color[0] < 220:
            starterColors.remove(BLUE)
            if itsThisOneChief:
                firstColor = BLUE
                itsThisOneChief = False
            else:
                lastColor = BLUE
        elif color[0] > 290 and color[0] < 360:
            starterColors.remove(RED)
            if itsThisOneChief:
                firstColor = RED
                itsThisOneChief = False
            else:
                lastColor = RED
    middleColor = [RED,GREEN,BLUE]
    middleColor.remove(firstColor)
    middleColor.remove(lastColor)
    COLOR_PRIORITY.append(firstColor)
    COLOR_PRIORITY.append(middleColor[0])
    COLOR_PRIORITY.append(lastColor)

def convertBGRtoHSV(BGR):
    b,g,r = BGR[:]/255
    v = max([b,g,r])
    s = 0 if v == 0 else (v-min([b,g,r]))/v

    if v is r:
        h = 60*(g-b)/(v-min([b,g,r]))
    elif v is g:
        h = 120 + 60*(g-b)/(v-min([b,g,r]))
    elif v is b:
        h = 240 + 60*(r-g)/(v-min([b,g,r]))
    h+=360 if h < 0 else 0
    
    v = np.round(255*v).astype(int)
    s = np.round(255*s).astype(int)
    h = np.round(180*h/s).astype(int)
    return [h,s,v]

def get_ar_markers(
    color_image: NDArray[(Any, Any, 3), np.uint8]
) -> Tuple[List[NDArray[(1, 4, 2), np.int32]], Optional[NDArray[(Any, 1), np.int32]]]:
    
    dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
    params = cv.aruco.DetectorParameters_create()

    corners, ids, _ = cv.aruco.detectMarkers(
        color_image,
        dictionary,
        parameters=params
    )
    return (corners, ids)

def followLine(color_priority):
    cCenter,cArea = updateContour(color_priority)
    if cCenter is not None:
        errorTerm = cCenter[1]-320
        angle = errorTerm/320
    else:
        angle = 0
    return rc_utils.clamp(angle*2,-1,1)

def updateContour(color_priority):
    image = rc.camera.get_color_image()
    if image is None:
        contour_center = None
        contour_area = 0
    else:
        image_cropped = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])
        for color in color_priority:
            contours = rc_utils.find_contours(image_cropped,color[0],color[1])
            if len(contours) > 0:
                break
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
        if contour is not None:
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)
        else:
            contour_center = None
            contour_area = 0
        rc.display.show_color_image(image)
        return contour_center,contour_area

def update_slow():
    pass #NOTHING TO DO HERE

if __name__ == "__main__":
    rc.set_start_update(start,update,update_slow)
    rc.go()
