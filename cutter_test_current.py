import time
from machine import Pin, ADC

class Cutter:
    # TODO: current measurement for stall detection, and/or lim switches
    # int pin numbers for the motor signal pins, and pin for measuring current 
    def __init__(self, dc_pin1, dc_pin2, measure_pin, lim_sw_open, lim_sw_closed):
        self.dc1 = Pin(dc_pin1, Pin.OUT)
        self.dc2 = Pin(dc_pin2, Pin.OUT)
        # use 11dB atten, which is good for measuring from 150-2450mV
        self.voltage_measure = ADC(Pin(measure_pin)) # default atten value?
        self.measurements = []
        self.measurement_threshold = 220 # tune to the cutter
        self.lim_open = Pin(lim_sw_open, Pin.IN, Pin.PULL_UP)
        self.lim_closed = Pin(lim_sw_closed, Pin.IN, Pin.PULL_UP)
        self.stalled = False

    def cut(self):
        # TODO: check for stalling and update bool
        # reset measurement array
        self.measurements = []
        while(not self.stalled):
            self.check_stall()
            self.dc1(1)
            self.dc2(0)
            time.sleep_ms(10) # keep the same for now -- relates to number of measurements to ignore at begining
        self.open_blades() # stop when stall detected

    def open_blades(self):
        while(self.lim_open.value()):
            self.dc1(0)
            self.dc2(1)
        self.stop()

    def stop(self):
        self.dc1(0)
        self.dc2(0)
    
    # TODO
    def check_stall(self):
        if not self.lim_closed.value():
            self.stalled = True
            print("hit stall limit sw")

        resistor_reading = self.voltage_measure.read()
        self.measurements.append(resistor_reading)

        if len(self.measurements) > 50:
            # get last 20 measurements
            last_20 = self.measurements[-20:]
            avg = sum(last_20)/len(last_20)
            print(avg)
            if avg > self.measurement_threshold:
                self.stalled = True
                print("measured a stall")

            
CUTTER_PIN1 = 15    
CUTTER_PIN2 = 2
CUTTER_MEASURE = 36
LIM_SW_OPEN = 26
LIM_SW_CLOSE = 25

# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE, LIM_SW_OPEN, LIM_SW_CLOSE)

print("cut time")
cutter.cut()