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