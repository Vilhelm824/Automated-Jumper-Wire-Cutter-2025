import time
from machine import Pin, reset
from bender import Bender
from extruder import Extruder
from cutter import Cutter
import sys


# button pins
BUTTON1_PIN = 27   # Extruder fwd
BUTTON2_PIN = 14   # Emergency stop
BUTTON3_PIN = 26    # Cutter close
BUTTON4_PIN = 25    # Cutter open
BUTTON5_PIN = 33    # Actuator down
BUTTON6_PIN = 32    # Actuator up
# cutter motor pins
CUTTER_PIN1 = 15    
CUTTER_PIN2 = 2
# cutter current measurement pin
CUTTER_MEASURE = 34
# stepper pins
STEPPER_PIN1 = 19
STEPPER_PIN2 = 18
STEPPER_PIN3 = 5
STEPPER_PIN4 = 17
# linear actuator pins
LIN_ACT_PIN1 = 0
LIN_ACT_PIN2 = 4
# limit switches for the linear actuator
LIM_SW_TOP = 22
LIM_SW_BOTTOM = 23


def emergency_stop_button(button):
    cutter.stop()
    actuator.stop()
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
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE)
# initialize actuator
actuator = Bender(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)


num_wires = int(input("number of wires: "))
jumper_length = float(input("jumper length: "))

try:
    ready = input("ready to go (y/n): ")
    if ready=="y":
        for i in range(num_wires):
            print("starting wire #", i+1)
            # extrude set amount
            extruder.extrude_length(jumper_length)
            print("done extruding, manually cut now")

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
            while(actuator.lim_bottom.value()):
                actuator.move_down()
            actuator.stop()
            print("finished moving down")
            time.sleep(1)
            while(actuator.lim_top.value()):
                actuator.move_up()
            actuator.stop()
            print("finished moving up")
            print("finished wire #", i+1)
            time.sleep(1)
    else:
        print("exiting")      
    cutter.stop()
    actuator.stop()
    extruder.release()
    print("done")

      
except KeyboardInterrupt:
    cutter.stop()
    actuator.stop()
    extruder.release()
    print("done")
except Exception as e:
    cutter.stop() 
    actuator.stop()
    extruder.release()
    print("Caught Exception: ", e)