class Bender:
    # int pin numbers for motor control and limit switches
    def __init__(self, act_pin1, act_pin2, lim_sw_top, lim_sw_bottom):
        # output pins for the linear actuator h-bridge
        self.la1 = Pin(act_pin1, Pin.OUT)
        self.la2 = Pin(act_pin2, Pin.OUT)
        # input pins for the limit switches
        self.lim_top = Pin(lim_sw_top, Pin.IN, Pin.PULL_UP)
        self.lim_bottom = Pin(lim_sw_bottom, Pin.IN, Pin.PULL_UP)
    
    def move_down(self):
        # prevent movement if at limit
        # pull up sw, so 1 when not pressed
        if self.lim_bottom.value():
            la1.value(1)
            la2.value(0)
        else:
            self.stop()

    def move_up(self):
        # prevent movement if at limit
        # pull up sw, so 1 when not pressed
        if self.lim_top.value():
            la1.value(0)
            la2.value(1)
        else:
            self.stop()
    
    def stop(self):
        la1.value(0)
        la2.value(0)