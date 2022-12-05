import digitalio
import busio
from board import *
from key_stroke import Key_stroke, mouse, kbd
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse2 import Mouse2
from adafruit_mcp230xx.mcp23017 import MCP23017

print('Left KM')
stroke_time = 0.00
cpi = 650

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
mouse_move_interconnect_out = digitalio.DigitalInOut(GP10)
mouse_move_interconnect_in = digitalio.DigitalInOut(GP11)
layer_2_interconnect_out = digitalio.DigitalInOut(GP12)
layer_2_interconnect_in = digitalio.DigitalInOut(GP13)
layer_3_interconnect_out = digitalio.DigitalInOut(GP14)
layer_3_interconnect_in = digitalio.DigitalInOut(GP15)
mouse_move_interconnect_out.direction = digitalio.Direction.OUTPUT
mouse_move_interconnect_in.direction = digitalio.Direction.INPUT
mouse_move_interconnect_in.pull = digitalio.Pull.DOWN
layer_2_interconnect_out.direction = digitalio.Direction.OUTPUT
layer_2_interconnect_in.direction = digitalio.Direction.INPUT
layer_2_interconnect_in.pull = digitalio.Pull.DOWN
layer_3_interconnect_out.direction = digitalio.Direction.OUTPUT
layer_3_interconnect_in.direction = digitalio.Direction.INPUT
layer_3_interconnect_in.pull = digitalio.Pull.DOWN
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

pin_order = [16, 18, 11, 10,  9, 8,
             27, 26, 25, 24,  5, 4,
             28, 29, 30, 31,  7, 6,
             21, 22, 15, 23, 13, 12,
             19, 20,          0, 1,
                              2, 3]  # found the issue 32 points but only 30 keys

layer_1 = [[Keycode.ESCAPE], ['1'], ['2'], ['3'], ['4'], ['5'],
           [Keycode.TAB], ['q'], ['w'], ['e'], ['r'], ['g'],
           [''], ['a'], ['s', Mouse.RIGHT_BUTTON], ['d', Mouse.MIDDLE_BUTTON], ['f', Mouse.LEFT_BUTTON], ['t'],
           [Keycode.SHIFT], ['z'], ['x'], ['c'], ['v'], ['b'],
           [Keycode.WINDOWS], [Keycode.ALT], [''], [Keycode.TAB],
           [Keycode.CONTROL], [Keycode.DELETE]]
layer_2 = [[Keycode.F1], [Keycode.F2], [Keycode.F3], [Keycode.F4], [Keycode.F5], [Keycode.F6],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [Mouse.RIGHT_BUTTON], [Mouse.MIDDLE_BUTTON], [Mouse.LEFT_BUTTON], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''],
           [''], ['']]
layer_3 = [[''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''],
           [''], ['']]
layer_4 = [[''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''], [''], [''],
           [''], [''], [''], [''],
           [''], ['']]

mouse_keys = [14, 15, 16]
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

    layer_2_key = keys[26]
    layer_3_key = keys[12]
