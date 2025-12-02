class Cutter:
    # TODO: current measurement for stall detection, and/or lim switches
    # int pin numbers for the motor signal pins, and pin for measuring current 
    def __init__(self, dc_pin1, dc_pin2, measure_pin, lim_sw_open):
        self.dc1 = Pin(dc_pin1, Pin.OUT)
        self.dc2 = Pin(dc_pin2, Pin.OUT)
        self.measure_v = Pin(measure_pin, Pin.IN)
        self.lim_open = Pin(lim_sw_open, Pin.IN, Pin.PULL_UP)
        self.stalled = False

    def close_blades(self):
        # TODO: check for stalling and update bool
        while(not stalled):
            self.dc1(1)
            self.dc2(0)
    
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