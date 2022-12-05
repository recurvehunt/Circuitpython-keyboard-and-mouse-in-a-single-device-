import time
from board import *
import digitalio
import pmw3389
import pins


class Led:
    def __init__(self):
        self.poll_timer = 0

    def blink(self):
        curr_time = time.monotonic()
        if curr_time > self.poll_timer:
            pins.led.value = not pins.led.value
            self.poll_timer = curr_time + 0.25


class MouseMovementDelay:
    def __init__(self):
        self.movement = False
        self.delay_off_time = .75
        self.last_movement_time = 0

    def reset_motion_clock(self):
        self.last_movement_time = time.monotonic()
        self.movement = True
        pins.mouse_move_interconnect_out.value = True

    def check_movement(self):
        if pins.layer_2_key.value or pins.layer_3_key.value:
            self.movement = False
            pins.mouse_move_interconnect_out.value = False
        elif pmw3389.right_mouse.is_moving:
            self.reset_motion_clock()
        elif time.monotonic() - self.last_movement_time > self.delay_off_time:
            self.movement = False
            pins.mouse_move_interconnect_out.value = False


def set_layer():
    pins.layer_2_interconnect_out.value = pins.layer_2_key.value
    pins.layer_3_interconnect_out.value = pins.layer_3_key.value
    if pins.layer_2_key.value and pins.layer_3_key.value:
        return 3
    elif pins.layer_2_key.value:
        return 1
    elif pins.layer_3_key.value:
        return 2
    else:
        return 0


led_indicator = Led()
mouse_key_movement_indication = MouseMovementDelay()
average_time = 0
mouse_interval = 0

while True:
    start = time.monotonic()
    led_indicator.blink()
    layer = set_layer()

    for key in pins.keys:
        key.mouse_is_moving = mouse_key_movement_indication.movement or pins.mouse_move_interconnect_in.value
        key.check(layer)
        #if key.value and key.is_mouse_button: # issue with the logic here, always passing true... will need to investigate later
        #    mouse_key_movement_indication.reset_motion_clock()
        if mouse_interval == 10:
            pmw3389.right_mouse.movement()
            mouse_key_movement_indication.check_movement()
            mouse_interval = 0
        else:
            mouse_interval = mouse_interval + 1

    #end = time.monotonic()
    #loop_time = end-start
    #average_time = average_time*.99 + loop_time*.01
    #if pins.led.value:
    #    print(average_time)

