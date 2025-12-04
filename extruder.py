import time
from machine import Pin

class Extruder:
    # TODO 
    # - add function(s) for extruding certain wire lengths - kinda done
    # - change the sleeps for delay to check time between steps instead--similar to debounce

    # int pin numbers that correspond to the stepper control pins
    def __init__(self, pin1, pin2, pin3, pin4, step_delay=0.06):
        # create pin objects
        self.step1 = Pin(pin1, Pin.OUT)
        self.step2 = Pin(pin2, Pin.OUT)
        self.step3 = Pin(pin3, Pin.OUT)
        self.step4 = Pin(pin4, Pin.OUT)
        # steps go: 0>1>2>3
        self.current_step = 0
        self.stepper_delay = step_delay
        # length to step conversion
        self.mm_per_step = 0.1175
        # tune num steps for correct wire lengths
        self.step_offset = -18
    
    # input length in inches for the jumper
    def extrude_length(self, length):
        length += 0.6 # add length of bent prongs
        length_in_mm = length * 25.4 # convert in to mm
        steps = int(length_in_mm / self.mm_per_step) + self.step_offset
        for i in range(steps):
            self.one_step()
    
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