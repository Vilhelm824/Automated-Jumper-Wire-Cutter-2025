import time
from machine import Pin, reset, I2C, Encoder
from lcd1602 import LCD
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
LIM_SW_CLOSED = 13
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

# control panel initializations
sda_pin = 21
scl_pin = 22
enc_out1 = 14
enc_out2 = 27
enc_switch = 26

# initialize encoder
encoder = Encoder(0, Pin(enc_out1, Pin.IN), Pin(enc_out2, Pin.IN))
enc_button = Pin(enc_switch, Pin.IN)
# initialize lcd
i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
lcd = LCD(i2c)

old_val = encoder.value()
num_wires = 0
wire_size = 0.3
button_state = False
num_finished = 0
cmd = "start"
screen_state = 0    # 1 is wire select, 2 is size select, 3 is continue, 4 is completed, 5 is pause, 0 is initial


# cursor setup
lcd.send_command(0x0D)
lcd.send_command(0x80)

lcd.clear()
lcd.write(0, 0, "-Start")
lcd.write(0, 1, "-Change Die")



stop_bender = False

def change_die():
    lcd.clear()
    lcd.write(0, 0, "Change Die Mode")
    lcd.write(0, 1, "Moving Down")
    bender.change_die()
    time.sleep(1)
    
    # wait for button press
    while enc_button.value() == 1:
        pass
    
    bender.move_up()


def emergency_stop_button(button):
    cutter.stop()
    bender.stop()
    extruder.release()
    reset()

# initialize stepper
extruder = Extruder(STEPPER_PIN1, STEPPER_PIN2, STEPPER_PIN3, STEPPER_PIN4, step_delay=0.02)
# initialize cutter
cutter = Cutter(CUTTER_PIN1, CUTTER_PIN2, CUTTER_MEASURE, LIM_SW_OPEN, LIM_SW_CLOSED)
# initialize bender
bender = Bender(LIN_ACT_PIN1, LIN_ACT_PIN2, LIM_SW_TOP, LIM_SW_BOTTOM)



selecting = True
running = True

try:
    while running:
        while selecting:
            current_val = encoder.value()
            if current_val != old_val:
                if screen_state == 0:
                    if cmd == "start":
                        lcd.send_command(0xC0)
                        cmd = "change_die"
                    else:
                        lcd.send_command(0x80)
                        cmd = "start"
                elif screen_state == 1:
                    if num_wires >= 50:
                        increment = 10
                    elif num_wires >= 10:
                        increment = 5
                    else:
                        increment = 1
                    if current_val > old_val:
                        num_wires += increment
                    else:
                        num_wires -= increment
                    if num_wires < 0:
                        num_wires = 0
                    string = "# Wires: " + str(num_wires)
                    lcd.write(9, 0, "    ")
                    lcd.write(0, 0, string)
                    lcd.send_command(0x89)
                elif screen_state == 2:
                    if current_val > old_val:
                        wire_size += 0.1
                    else:
                        wire_size -= 0.1
                    if wire_size < 0.2:
                        wire_size = 0.2
                    elif wire_size > 2:
                        wire_size = 2
                    
                    wire_size = round(wire_size, 1)	
                        
                    lcd.write(6, 1, "      ")
                    lcd.write(0, 1, "Size: " + str(wire_size) + '"')
                    lcd.send_command(0xC6)
                
                elif screen_state == 3:
                    if cmd == "start_y":
                        lcd.send_command(0xC9)
                        cmd = "start_n"
                    else:
                        lcd.send_command(0xC7)
                        cmd = "start_y"
                        
                elif screen_state == 5:
                    if cmd == "resume":
                        lcd.send_command(0xCA)
                        cmd = "stop"
                    else:
                        lcd.send_command(0xC0)
                        cmd = "resume"
                old_val = current_val
                
                        
            if enc_button.value() == 0 and button_state == False:
                button_state = True
                #print("button pressed, command:", cmd)
                
                if screen_state == 0:
                    if cmd == "start":
                        screen_state = 1
                        lcd.clear()
                        lcd.write(0, 0, "# Wires: " + str(num_wires))
                        lcd.write(0, 1, "Size: " + str(wire_size) + '"')
                        lcd.send_command(0x89)
                    else:
                        change_die()
                        lcd.clear()
                        lcd.write(0, 0, "-Start")
                        lcd.write(0, 1, "-Change Die")
                        lcd.send_command(0x80)
                        cmd = "start"
                
                # screen state 1 = picking number of wires
                elif screen_state == 1:
                    screen_state = 2
                    lcd.send_command(0xC6)
                
                # screen state 2 = picking wire size
                elif screen_state == 2:
                    screen_state = 3
                    lcd.clear()
                    lcd.write(0, 0, str(num_wires) + " wires, " + str(wire_size) + '"')
                    lcd.write(0, 1, "Start: Y N")
                    lcd.send_command(0xC7)
                    cmd = "start_y"
                    
                # screen state 3 = ask to start
                elif screen_state == 3 and cmd == "start_y":
                    screen_state = 4
                    lcd.clear()
                    lcd.write(0, 0, "Completed " + str(num_finished) + " / " + str(num_wires))
                    lcd.write(0, 1, "-Pause")
                    lcd.send_command(0xC0)
                    selecting = False
                
                # screen state 4 = show current finished wires
                elif screen_state == 4:
                    screen_state = 5
                    cmd = "resume"
                    lcd.clear()
                    lcd.write(0, 0, "Paused")
                    lcd.write(0, 1, "-Resume | -Stop")
                    lcd.send_command(0xC0)
                
                # screen state 5 = pause screen, resume or stop
                elif screen_state == 5:
                    if cmd == "resume":
                        screen_state = 4
                        lcd.clear()
                        lcd.write(0, 0, "Completed " + str(num_finished) + " / " + str(num_wires))
                        lcd.write(0, 1, "-Pause")
                        lcd.send_command(0xC0)
                    else:
                        screen_state = 0
                        lcd.clear()
                        lcd.write(0, 0, "-Start")
                        lcd.write(0, 1, "-Change Die")
                        lcd.send_command(0x80)
                        cmd = "start"
                else:
                    screen_state = 0
                    lcd.clear()
                    lcd.write(0, 0, "-Start")
                    lcd.write(0, 1, "-Change Die")
                    lcd.send_command(0x80)
                    cmd = "start"
                    
            if enc_button.value() == 1 and button_state == True:
                button_state = False
                time.sleep(0.5)

        print("going to make", num_wires, "at", wire_size)
        #input()
        
        for i in range(num_wires):
            # make sure bender is moved to the top and cutter blades are open
            # before extruding
            print("making sure bender and cutter are out of the way")
            bender.move_up()
            cutter.open_blades()
            # extrude the jumper length (added length of jumper legs is taken care of in Extruder class)
            print("extruding")
            time.sleep(1)
            extruder.extrude_length(wire_size)
            print("done extruding, cutting now")
            time.sleep(1)
            cutter.cut()
            print("done cutting, bending now")
            time.sleep(1)
            bender.move_down()
            print("Moving back up")
            time.sleep(1)
            bender.move_up()
            print("finished wire #", i+1)
            num_finished += 1
            lcd.write(0, 0, "Completed " + str(num_finished) + " / " + str(num_wires))
            time.sleep(1)
        
        num_finished = 0
        screen_state = 0
        lcd.clear()
        lcd.write(0, 0, "-Start")
        lcd.write(0, 1, "-Change Die")
        lcd.send_command(0x80)
        cmd = "start"
        selecting = True
        
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
    lcd.clear()
    print("done cleaning up")