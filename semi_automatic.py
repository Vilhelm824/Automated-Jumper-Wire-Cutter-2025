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
extruder = Extruder(STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4)
# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE, LIM_SW_OPEN, LIM_SW_CLOSED)
# initialize bender
bender = Bender(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)


jumper_length = float(input("jumper length: "))
num_jumpers = int(input("number of jumpers: "))

try:
    ready = input("ready to go (y/n): ")
    if ready=="y":
        bender.move_up()
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
