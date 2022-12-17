import digitalio
import busio
from board import *
from key_stroke import Key_stroke, mouse, kbd
from adafruit_hid.keycode import Keycode
from pan_mouse import PanMouse
from adafruit_mcp230xx.mcp23017 import MCP23017

print('Right KM')
stroke_time = 0.00
cpi = 450

sda = GP0
scl = GP1
# p2 = GP2 unused
# p3 = GP3 unused
# p4 = GP4 unused
cs_left = digitalio.DigitalInOut(GP5)  # not connected
# p6 = GP6 unused
# p7 = GP7 unused
# p8 = GP8 unused
# p9 = GP9 unused
mouse_move_interconnect_in = digitalio.DigitalInOut(GP10)
mouse_move_interconnect_out = digitalio.DigitalInOut(GP11)
layer_2_interconnect_in = digitalio.DigitalInOut(GP12)
layer_2_interconnect_out = digitalio.DigitalInOut(GP13)
layer_3_interconnect_in = digitalio.DigitalInOut(GP14)
layer_3_interconnect_out = digitalio.DigitalInOut(GP15)
mouse_move_interconnect_in.direction = digitalio.Direction.INPUT
mouse_move_interconnect_in.pull = digitalio.Pull.DOWN
mouse_move_interconnect_out.direction = digitalio.Direction.OUTPUT
layer_2_interconnect_in.direction = digitalio.Direction.INPUT
layer_2_interconnect_in.pull = digitalio.Pull.DOWN
layer_2_interconnect_out.direction = digitalio.Direction.OUTPUT
layer_3_interconnect_in.direction = digitalio.Direction.INPUT
layer_3_interconnect_in.pull = digitalio.Pull.DOWN
layer_3_interconnect_out.direction = digitalio.Direction.OUTPUT
MISO = GP16
cs_right = digitalio.DigitalInOut(GP17)
SCK = GP18
MOSI = GP19
# p20 = GU20 unused
# p21 = GP21 unused
# p22 = GP22 unused

# p26 = GP26 unused
# p27 = GP27 unused
# p28 = GP28 unused

led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(scl, sda)
mcp_20 = MCP23017(i2c)
mcp_21 = MCP23017(i2c, address=0x21)

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Now call the get_pin function to get an instance of a pin on the chip.
# This instance will act just like a digitalio.DigitalInOut class instance
# and has all the same properties and methods (except you can't set pull-down
# resistors, only pull-up!).  For the MCP23017 you specify a pin number from
# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).


def setup_mcp23017_pins(device):
    list_of_pins = []
    for pin_num in range(0, 16):
        list_of_pins.append(device.get_pin(pin_num))
        list_of_pins[pin_num].direction = digitalio.Direction.INPUT
        list_of_pins[pin_num].pull = digitalio.Pull.UP
    return list_of_pins


mcp_pins = []
for mcp in [mcp_20, mcp_21]:
    mcp_pins.extend(setup_mcp23017_pins(mcp))

pin_order = [12, 0, 4, 21, 29, 24,
             13, 1, 5, 20, 30, 25,
             14, 2, 6, 19, 31, 26,
             15, 3, 7, 18, 23, 27,
             8, 9,         22, 28,
             10, 11]  # found the issue 32 points but only 30 keys

layer_1 = [['6'], ['7'], ['8', '8'], ['9'], ['0'], [Keycode.BACKSPACE],
           ['y'], ['j',                ''], ['k',                  ''], ['l',                 ''], ['p', ''], ['['],
           ['h'], ['u', PanMouse.LEFT_BUTTON], ['i', PanMouse.MIDDLE_BUTTON], ['o', PanMouse.RIGHT_BUTTON], [';'], ["'"],
           ['n'], ['m'], [','], ['.'], ['/'], [Keycode.SHIFT],
           [''], [Keycode.SPACE], [Keycode.ALT], [Keycode.WINDOWS],
           [Keycode.BACKSPACE], [Keycode.ENTER]]
layer_2 = [[Keycode.F7], [Keycode.F8], [Keycode.F9], [Keycode.F10], [Keycode.F11], [Keycode.F12],
           [''], [''], [Keycode.UP_ARROW], [''], [''], [''],
           [''], [Keycode.LEFT_ARROW], [Keycode.DOWN_ARROW], [Keycode.RIGHT_ARROW], [''], [''],
           [''], [''], [''], [''], ['\\'], [''],
           [''], [''], [''], [''],
           [''], ['']]
layer_3 = [[''], [''], [''], [''], [''], ['-'],
           [''], [''], [''], [''], [''], [']'],
           [''], [''], [''], [''], ['+'], ['='],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''],
           [''], ['']]
layer_4 = [[''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''],
           [''], ['']]

mouse_keys = [13, 14, 15]
keys = []

i = 0
for pin_number in pin_order:  # should be able to combine with above for loop but will keep separate for now
    try:
        keys.append(Key_stroke(mcp_pins[pin_number], stroke_time))
        keys[i].key = [layer_1[i], layer_2[i], layer_3[i], layer_4[i]]

    except IndexError:
        print('list ran out before pins did')
    i = i + 1

for key_number in mouse_keys:
    keys[key_number].is_mouse_button = True

    layer_2_key = layer_2_interconnect_in
    layer_3_key = layer_3_interconnect_in

