"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""

########################################################################################
# Imports
########################################################################################

import sys
import math
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Globals
counter = 0;
isDriving = False;
isA = False;
isB = False;
isX = False;
isY = False;

########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # If we use a global variable in our function, we must list it at
    # the beginning of our function like this 
    global counter
    global isDriving
    global isA
    global isB
    global isX
    global isY

    # The start function is a great place to give initial values to global variables
    counter = 0;
    isDriving = False;
    isA = False;
    isB = False;
    isX = False;
    isY = False;

    # Begin at a full stop
    rc.drive.stop()

    # Print start message
    # TODO (main challenge): add a line explaining what the Y button does
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "   Right trigger = accelerate forward\n"
        "   Left trigger = accelerate backward\n"
        "   Left joystick = turn front wheels\n"
        "   A button = drive a circle\n"
        "   B button = drive a square\n"
        "   X button = drive a figure eight\n"
	"   Y button = drive a spiral\n"
    )

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO (warmup): Implement acceleration and steering
    # rc.drive.set_speed_angle(0, 0)
    global counter
    global isDriving
    global isA
    global isB
    global isX
    global isY

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Starting to drive a circle...");                                                                                 counter = 0;                                                                                                            isDriving = True;                                                                                                       isA = True;                                                                                                             isB = False;                                                                                                            isX = False;                                                                                                            isY = False; 
    elif rc.controller.was_pressed(rc.controller.Button.B):
        print("Starting to drive a square...");
        counter = 0;
        isDriving = True;
        isA = False;
        isB = True;
        isX = False;
        isY = False;
    elif rc.controller.was_pressed(rc.controller.Button.X):
        print("Starting to drive a figure eight...");
        counter = 0;
        isDriving = True;
        isA = False;
        isB = False;
        isX = True;
        isY = False;
    elif rc.controller.was_pressed(rc.controller.Button.Y):
        print("Starting to drive a spiral...");                                                                                 counter = 0;                                                                                                            isDriving = True;                                                                                                       isA = False;                                                                                                            isB = False;                                                                                                            isX = False;                                                                                                            isY = True;

    if isDriving:
         counter += rc.get_delta_time();
         if isA:
            if counter < 11.38:
                # TODO (main challenge): Drive in a circle when button A is pressed
                rc.drive.set_speed_angle(0.5, 1.0); # full right at 0.5 speed forward
            else: #stop
                isDriving = False;
                isA = False;
                print("Stopping...");
                rc.drive.stop();
                counter = 0;
         elif isB:
            turnConst = 2.835
            if counter < 3:
                rc.drive.set_speed_angle(-1,0)
            elif counter < 10:
                rc.drive.set_speed_angle(0.43,0)
            elif counter < 10+turnConst:
                rc.drive.set_speed_angle(0.43, 1.0); # full right at 0.1 speed forward
            elif counter < 12+turnConst: #+3
                rc.drive.set_speed_angle(0.43, 0.0); # streight forward at 0.1 speed forward
            elif counter < 12+2*turnConst: #+2.381
                rc.drive.set_speed_angle(0.43, 1.0); # full right at 0.1 speed forward
            elif counter < 14+2*turnConst: #+3
                rc.drive.set_speed_angle(0.43, 0.0); # streight forward at 0.1 speed forward
            elif counter < 14+3*turnConst: #+2.381
                rc.drive.set_speed_angle(0.43, 1.0); # full right at 0.1 speed forward 
            elif counter < 16+3*turnConst: #+3
                rc.drive.set_speed_angle(0.43, 0.0); # full right at 0.1 speed forward
            elif counter < 16+4*turnConst: #+2.431
                rc.drive.set_speed_angle(0.43, 1.0); # full right at 0.1 speed forward
            elif counter < 18+4*turnConst: #+0.5
                rc.drive.set_speed_angle(0.43, 0.0); # full right at 0.1 speed forward 
            else :
                print("Stopping...");
                isDriving = False;
                isB = False;
                rc.drive.stop();
                counter = 0;
         elif isX:
            turnConst = 5.2
            if counter < 5:
                rc.drive.set_speed_angle(-1,0);
            elif counter < 7:
                rc.drive.stop();
            elif counter < 9:
                rc.drive.set_speed_angle(0.5,0);
            elif counter < 9+turnConst+0.1:
                rc.drive.set_speed_angle(0.5,-1);
            elif counter < 9+3*turnConst+0.1:
                rc.drive.set_speed_angle(0.5,1)
            elif counter < 9+4*turnConst+0.1:
                rc.drive.set_speed_angle(0.5,-1)
            else:
                isDriving = False;                                                                                                      isX = False;                                                                                                            print("Stopping...");                                                                                                   rc.drive.stop();                                                                                                        counter = 0;
         elif isY:
             angle = 1- math.sqrt(counter)/math.sqrt(20)
             if counter < 20:
                 rc.drive.set_speed_angle(1,angle)
             else:
                 isDriving = False
                 isY = False
                 print("Stopping...")
                 rc.drive.stop()
                 counter = 0


    # TODO (main challenge): Drive in a figure eight when the X button is pressed

    # TODO (main challenge): Drive in a shape of your choice when the Y button
    # is pressed


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
