import time
from machine import Pin, reset
from bender import Bender
from extruder import Extruder
from cutter import Cutter
import sys


# cutter motor pins
CUTTER_PIN1 = 15    
CUTTER_PIN2 = 2
# cutter current measurement pin
CUTTER_MEASURE = 36
# limit switches for the cutter 
LIM_SW_OPEN = 25
LIM_SW_CLOSED = 26
# linear bender pins
LIN_ACT_PIN1 = 0
LIN_ACT_PIN2 = 4
# limit switches for the linear bender
LIM_SW_TOP = 32
LIM_SW_BOTTOM = 33
# stepper pins
STEPPER_PIN1 = 19
STEPPER_PIN2 = 18
STEPPER_PIN3 = 5
STEPPER_PIN4 = 17


def emergency_stop_button(button):
    cutter.stop()
    bender.stop()
    extruder.release()
    reset()

# initialize stepper
extruder = Extruder(STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4, step_delay=0.04)
# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE, LIM_SW_OPEN, LIM_SW_CLOSED)
# initialize bender
bender = Bender(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)


jumper_length = float(input("jumper length: "))
num_jumpers = int(input("number of jumpers: "))

try:
    ready = input("ready to go (y/n): ")
    if ready=="y":
        for i in range(num_jumpers):
            # make sure bender is moved to the top and cutter blades are open
            # before extruding
            print("making sure bender and cutter are out of the way")
            bender.move_up()
            cutter.open_blades()
            # extrude the jumper length (added length of jumper legs is taken care of in Extruder class)
            print("extruding")
            time.sleep(1)
            extruder.extrude_length(jumper_length)
            print("done extruding, cutting now")
            time.sleep(1)
            cutter.cut()
            print("done cutting, bending now")
            time.sleep(1)
            bender.move_down()
            print("Moving back up")
            time.sleep(1)
            bender.move_up()
            print("finished wire #", i+1)
            time.sleep(1)
    else:
        print("exiting")      

      
except KeyboardInterrupt:
    print("keyboard interrupt")
except Exception as e:
    print("Caught Exception: ", e)
finally:
    cutter.stop()
    bender.stop()
    extruder.release()
    print("done cleaning up")