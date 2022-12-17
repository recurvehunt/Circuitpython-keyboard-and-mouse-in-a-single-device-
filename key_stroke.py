import usb_hid, time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
#from adafruit_hid.mouse import Mouse
from pan_mouse import PanMouse

mouse = PanMouse(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)


class Key_stroke:
    def __init__(self, pin, stroke_time):
        self.pin = pin
        self.key = ''
        self.time = 0
        self.tap_count = 0
        self.key_release = True
        self.modifier = 0
        self.key_fired = False
        self.key_return = ''
        #self.multikey = False  # having an value is equal to True, and True = 1
        self.stroke_time = stroke_time
        self.value = False
        self.codes = ''
        self.keyboard_mouse = ''
        self.is_mouse_button = False
        self.mouse_is_moving = False

    def check(self, modifier):
        def refresh_values():
            self.value = not self.pin.value
            self.modifier = modifier

        def mouse_key_check():
            if self.mouse_is_moving and self.is_mouse_button:
                self.tap_count = self.tap_count + 1

        def firing_key():
            self.key_release = False
            # multikey_check()
            mouse_key_check()
            self.key_fired = True
            self.fire_release(fire=True)

        def key_has_been_tapped():  # probably not going to use this
            self.tap_count = self.tap_count + 1
            self.key_release = False
            self.time = time.monotonic() + self.stroke_time

        # def multikey_check():  # may rename this if I use mouse movement status instead
        #    if self.multikey:
        #        self.tap_count = self.tap_count + self.multikey.value

        def key_pressed_but_yet_to_be_fired():
            if self.tap_count > 0 and time.monotonic() > self.time:
                firing_key()
            elif self.key_release:
                key_has_been_tapped()
            else:
                pass

        def key_not_pressed():
            self.key_release = True
            if self.key_fired:
                self.fire_release(fire=False)
                self.tap_count = 0
                self.key_fired = False

        refresh_values()
        if self.value and not self.key_fired:
            key_pressed_but_yet_to_be_fired()
        if not self.value:
            key_not_pressed()

    def fire_release(self, fire):
        def determine_what_key_to_send():
            try:
                self.key_return = self.key[self.modifier][self.tap_count - 1]
            except IndexError:
                self.key_return = self.key[- 1][-1]
                # return last value in array, there are still some Nonetype getting though

        def determine_what_the_keycode_is_and_the_device():
            if isinstance(self.key_return, str):
                try:
                    self.codes = layout.keycodes(self.key_return)
                    self.keyboard_mouse = kbd
                except TypeError:
                    return
            else:
                self.codes = [self.key_return]
                if self.key_return <= 4:
                    self.keyboard_mouse = mouse
                else:
                    self.keyboard_mouse = kbd

        if fire:
            determine_what_key_to_send()
            determine_what_the_keycode_is_and_the_device()

        for code in self.codes:
            if fire:
                self.keyboard_mouse.press(code)
            else:
                self.keyboard_mouse.release(code)
