import time
from machine import Pin, ADC

class Cutter:
    # TODO: current measurement for stall detection, and/or lim switches
    # int pin numbers for the motor signal pins, and pin for measuring current 
    def __init__(self, dc_pin1, dc_pin2, measure_pin, lim_sw_open):
        self.dc1 = Pin(dc_pin1, Pin.OUT)
        self.dc2 = Pin(dc_pin2, Pin.OUT)
        # use 11dB atten, which is good for measuring from 150-2450mV
        self.voltage_measure = ADC(Pin(measure_pin), atten=ADC.ATTN_11DB)
        self.lim_open = Pin(lim_sw_open, Pin.IN, Pin.PULL_UP)
        self.stalled = False

    def close_blades(self):
        # TODO: check for stalling and update bool
        while(not self.stalled):
            check_stall()
            self.dc1(1)
            self.dc2(0)
            time.sleep_ms(10)
        self.stop() # stop when stall detected

    def open_blades(self):
        self.dc1(0)
        self.dc2(1)

    # for automating opening process with lim sw, uncomment when ready
    # def open_blades(self):
    #     while(self.lim_open.value()):
    #         self.dc1(0)
    #         self.dc2(1)
    #     self.stop()

    def stop(self):
        self.dc1(0)
        self.dc2(0)
    
    # TODO
    def check_stall():
        pass