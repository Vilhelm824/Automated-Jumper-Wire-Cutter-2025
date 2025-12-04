import time
from machine import Pin, reset
from bender import Bender
from extruder import Extruder
from cutter import Cutter
import sys


# button pins
BUTTON1_PIN = 27
BUTTON2_PIN = 14
BUTTON3_PIN = 26
BUTTON4_PIN = 25
BUTTON5_PIN = 33
BUTTON6_PIN = 32
# cutter motor pins
CUTTER_PIN1 = 15    
CUTTER_PIN2 = 2
# cutter current measurement pin
CUTTER_MEASURE = 34
# cutter limit switch
LIM_SW_OPEN = 24
# stepper pins
STEPPER_PIN1 = 19
STEPPER_PIN2 = 18
STEPPER_PIN3 = 5
STEPPER_PIN4 = 17
# linear bender pins
LIN_ACT_PIN1 = 0
LIN_ACT_PIN2 = 4
# limit switches for the linear bender
LIM_SW_TOP = 22
LIM_SW_BOTTOM = 23


def emergency_stop_button(button):
    cutter.stop()
    bender.stop()
    extruder.release()
    reset()


# initialize buttons
button1 = Pin(BUTTON1_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON2_PIN, Pin.IN, Pin.PULL_UP)
button3 = Pin(BUTTON3_PIN, Pin.IN, Pin.PULL_UP)
button4 = Pin(BUTTON4_PIN, Pin.IN, Pin.PULL_UP)
button5 = Pin(BUTTON5_PIN, Pin.IN, Pin.PULL_UP)
button6 = Pin(BUTTON6_PIN, Pin.IN, Pin.PULL_UP)

button2.irq(trigger=Pin.IRQ_FALLING, handler=emergency_stop_button)

# initialize stepper
extruder = Extruder(STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4)
# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE, LIM_SW_OPEN)
# initialize bender
bender = Bender(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)


jumper_length = float(input("jumper length: "))

try:
    ready = input("ready to go (y/n): ")
    if ready=="y":
        # make sure bender is moved to the top
        bender.move_up()
        # extrude the jumper length (added length of jumper legs taken care of in Extruder class)
        extruder.extrude_length(jumper_length)
        print("done extruding, manually cut now")
        # TODO: this stuff should be changed to work auto with current measurement
        # pseudo code, assuming the sensing/limiting taken care of in cutter class
        # cutter.close()
        # cutter.open()
        has_cut = False
        while(not has_cut):
            # Cutter Control   
            if button3.value() == False:
                cutter.close_blades()
            elif button4.value() == False:
                cutter.open_blades()
            else:
                cutter.stop()
            # exit button
            if not button5.value():
                has_cut = True
                print("finished cutting")
        bender.move_down()
        print("finished moving down")
        time.sleep(1)
        bender.move_up()
        print("finished moving up")
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