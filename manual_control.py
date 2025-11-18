import time
from machine import Pin


# button pins
BUTTON1_PIN = 27   # Extruder fwd
BUTTON2_PIN = 14   # Extruder bckwd
BUTTON3_PIN = 26    # Cutter close
BUTTON4_PIN = 25    # Cutter open
BUTTON5_PIN = 32    # Actuator down
BUTTON6_PIN = 33    # Actuator up
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
LIM_SW_TOP = 36
LIM_SW_BOTTOM = 39


class Extruder:
    # TODO 
    # - add function(s) for extruding certain wire lengths
    # - change the sleeps for delay to check time between steps instead--similar to debounce

    # int pin numbers that correspond to the stepper control pins
    def __init__(self, pin1, pin2, pin3, pin4, step_delay=0.03):
        # create pin objects
        self.step1 = Pin(pin1, Pin.OUT)
        self.step2 = Pin(pin2, Pin.OUT)
        self.step3 = Pin(pin3, Pin.OUT)
        self.step4 = Pin(pin4, Pin.OUT)
        # steps: 0>1>2>3
        self.current_step = 0
        self.stepper_delay = step_delay
    
    def release(self):
        self.step1.value(0)
        self.step2.value(0)
        self.step3.value(0)
        self.step4.value(0)
    
    def one_step(self):
        self.current_step += 1
        self.current_step = self.current_step % 4
        
        if self.current_step == 0:
            # go to step 0
            self.step1.value(1)
            self.step2.value(0)
            self.step3.value(0)
            self.step4.value(1)
        elif self.current_step == 1:
            # go to step 1
            self.step1.value(1)
            self.step2.value(0)
            self.step3.value(1)
            self.step4.value(0)
        elif self.current_step == 2:
            # go to step 2
            self.step1.value(0)
            self.step2.value(1)
            self.step3.value(1)
            self.step4.value(0)
        elif self.current_step == 3:
            # go to step 3
            self.step1.value(0)
            self.step2.value(1)
            self.step3.value(0)
            self.step4.value(1)
        time.sleep(self.stepper_delay)
            
    def one_step_back(self):
        self.current_step -= 1
        self.current_step = self.current_step % 4
        
        if self.current_step == 0:
            # go to step 0
            self.step1.value(1)
            self.step2.value(0)
            self.step3.value(0)
            self.step4.value(1)
        elif self.current_step == 1:
            # go to step 1
            self.step1.value(1)
            self.step2.value(0)
            self.step3.value(1)
            self.step4.value(0)
        elif self.current_step == 2:
            # go to step 2
            self.step1.value(0)
            self.step2.value(1)
            self.step3.value(1)
            self.step4.value(0)
        elif self.current_step == 3:
            # go to step 3
            self.step1.value(0)
            self.step2.value(1)
            self.step3.value(0)
            self.step4.value(1)
        time.sleep(self.stepper_delay)



class Cutter:
    # int pin numbers for the motor signal pins, and pin for measuring current 
    def __init__(self, dc_pin1, dc_pin2, measure_pin):
        self.dc1 = Pin(dc_pin1, Pin.OUT)
        self.dc2 = Pin(dc_pin2, Pin.OUT)
        self.measure_v = Pin(measure_pin, Pin.IN)

    def close_blades(self):
        self.dc1(1)
        self.dc2(0)
    
    def open_blades(self):
        self.dc1(0)
        self.dc2(1)

    def stop(self):
        self.dc1(0)
        self.dc2(0)



class Actuator:
    # int pin numbers for motor control and limit switches
    def __init__(self, act_pin1, act_pin2, lim_sw_top, lim_sw_bottom):
        self.la1 = Pin(act_pin1, Pin.OUT)
        self.la2 = Pin(act_pin2, Pin.OUT)
        self.lim_top = Pin(lim_sw_top, Pin.IN, Pin.PULL_UP)
        self.lim_bottom = Pin(lim_sw_bottom, Pin.IN, Pin.PULL_UP)
    
    def move_down(self):
        # pull up sw, so 1 when not pressed
        if self.lim_bottom.value():
            la1.value(1)
            la2.value(0)
        else:
            print("at limit sw")
            self.stop()

    def move_up(self):
        # pull up sw, so 1 when not pressed
        if self.lim_bottom.value():
            la1.value(0)
            la2.value(1)
        else:
            self.stop()
            print("at limit sw")

    def stop(self):
        la1.value(0)
        la2.value(0)



# initialize buttons
button1 = Pin(BUTTON1_PIN, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON2_PIN, Pin.IN, Pin.PULL_UP)
button3 = Pin(BUTTON3_PIN, Pin.IN, Pin.PULL_UP)
button4 = Pin(BUTTON4_PIN, Pin.IN, Pin.PULL_UP)
button5 = Pin(BUTTON5_PIN, Pin.IN, Pin.PULL_UP)
button6 = Pin(BUTTON6_PIN, Pin.IN, Pin.PULL_UP)

# initialize stepper
extruder = Extruder(STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4)
# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE)
# initialize actuator
actuator = Actuator(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)

try:
    while True:
        # Extruder Control
        if button1.value() == False:
            extruder.one_step()
        elif button2.value() == False:
            extruder.one_step_back()

        # Cutter Control   
        if button3.value() == False:
            cutter.close_blades()
        elif button4.value() == False:
            cutter.open_blades()
        else:
            cutter.stop()

        # Actuator Control
        if button5.value() == False:
            actuator.move_down()
        elif button6.value() == False:
            actuator.move_up()
        else:
            actuator.stop()
      
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