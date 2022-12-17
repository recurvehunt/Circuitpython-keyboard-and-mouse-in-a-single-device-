import busio # https://www.w3schools.com/python/trypython.asp?filename=demo_default
from board import *
from adafruit_bus_device.spi_device import SPIDevice
import usb_hid
import time
import digitalio
import pmw3389_firmware
from key_stroke import mouse  # only one instance of mouse and keyboard to prevent glitches
import pins
from adafruit_hid.keycode import Keycode

spi = busio.SPI(GP18, MOSI=GP19, MISO=GP16)
#cs = digitalio.DigitalInOut(GP17) # this line will need to be removed

Product_ID = 0x00
Revision_ID = 0x01
Motion = 0x02
Delta_X_L = 0x03
Delta_X_H = 0x04
Delta_Y_L = 0x05
Delta_Y_H = 0x06
SQUAL = 0x07
Raw_Data_Sum = 0x08
Maximum_Raw_data = 0x09
Minimum_Raw_data = 0x0A
Shutter_Lower = 0x0B
Shutter_Upper = 0x0C
Control = 0x0D
Resolution_L = 0x0E
Resolution_H = 0x0F
Config2 = 0x10
Angle_Tune = 0x11
Frame_Capture = 0x12
SROM_Enable = 0x13
Run_Downshift = 0x14
Rest1_Rate_Lower = 0x15
Rest1_Rate_Upper = 0x16
Rest1_Downshift = 0x17
Rest2_Rate_Lower = 0x18
Rest2_Rate_Upper = 0x19
Rest2_Downshift = 0x1A
Rest3_Rate_Lower = 0x1B
Rest3_Rate_Upper = 0x1C
Observation = 0x24
Data_Out_Lower = 0x25
Data_Out_Upper = 0x26
SROM_ID = SROM_Version = 0x2A
Min_SQ_Run = 0x2B
Raw_Data_Threshold = 0x2C
Control2 = 0x2D
Config5_L = 0x2E
Config5_H = 0x2F
Power_Up_Reset = 0x3A
Shutdown = 0x3B
Inverse_Product_ID = 0x3F
LiftCutoff_Tune3 = 0x41
Angle_Snap = 0x42
LiftCutoff_Tune1 = 0x4A
Motion_Burst = 0x50
SROM_Load_Burst = 0x62
Lift_Config = 0x63
Raw_Data_Burst = 0x64
LiftCutoff_Tune2 = 0x65
LiftCutoff_Cal_Timeout = 0x71
LiftCutoff_Cal_Min_Length = 0x72
PWM_Period_Cnt = 0x73
PWM_Width_Cnt = 0x74

# add motion interupt pin later so you don't have to pollj


class PMW3389:
    def __init__(self, cs):
        self.cs = cs
        self.device = SPIDevice(spi, cs, baudrate=8000000, polarity=1, phase=1)
        self.perform_startup()
        time.sleep(0.5)
        self.disp_registers()
        self.is_moving = False
        self.mouse_x_move_history = [0] * 10
        self.mouse_y_move_history = [0] * 10

    def adns_com_begin(self):
        self.cs.value = False

    def adns_com_end(self):
        self.cs.value = True

    def adns_write_reg(self, address, data):
        with self.device as bus:
            bus.write(bytearray([address | 0x80, data]))

    def adns_read_reg(self, address, array_size=1):
        with self.device as bus:
            bus.write(bytearray([address & 0x7f]))
            data = bytearray(array_size)
            bus.readinto(data)
        return data

    def adns_upload_firmware(self):
        print("Uploading firmware...")
        self.adns_write_reg(Config2, 0x00)
        self.adns_write_reg(SROM_Enable, 0x1d)
        time.sleep(0.01)
        self.adns_write_reg(SROM_Enable, 0x18)
        with self.device as bus:
            bus.write(bytearray([SROM_Load_Burst | 0x80]))
            time.sleep(0.000015)
            for data in pmw3389_firmware.data:
                bus.write(bytearray([data]))
                time.sleep(0.000015)
        self.adns_read_reg(SROM_ID)
        self.adns_write_reg(Config2, 0x00)  # set to 0x20 for wireless mouse design

    def perform_startup(self):
        self.adns_com_end()
        self.adns_com_begin()
        self.adns_com_end()
        self.adns_write_reg(Shutdown, 0xb6)
        time.sleep(.3)
        self.adns_com_begin()
        time.sleep(0.04)
        self.adns_com_end()
        time.sleep(0.04)
        self.adns_write_reg(Power_Up_Reset, 0x5a)
        time.sleep(0.5)
        self.adns_read_reg(Motion)
        self.adns_read_reg(Delta_X_L)
        self.adns_read_reg(Delta_X_H)
        self.adns_read_reg(Delta_Y_L)
        self.adns_read_reg(Delta_Y_H)
        self.adns_upload_firmware()
        time.sleep(0.01)
        self.set_cpi(pins.cpi)  # new set to 400, 800, 1200, or, 1600
        print("Optical Chip Initialized")

    def update_point(self):
        self.adns_write_reg(Motion, 0x01)  # write 0x01 to Motion register and read from it to freeze the motion values and make them available
        self.adns_read_reg(Motion)
        x = self.adns_read_reg(Delta_X_H)[0] << 8 | self.adns_read_reg(Delta_X_L)[0]
        y = self.adns_read_reg(Delta_Y_H)[0] << 8 | self.adns_read_reg(Delta_Y_L)[0]
        return x, y

    def set_cpi(self, cpi):
        cpival = int(cpi / 50)
        self.adns_write_reg(Resolution_L, (cpival & 0xFF))
        self.adns_write_reg(Resolution_H, ((cpival >> 8) & 0xFF))

    def disp_registers(self):
        oreg = [0x00, 0x3F, 0x2A, 0x02]
        oregname = ["Product_ID", "Inverse_Product_ID", "SROM_Version", "Motion"]
        signature = [0x42, 0xBD, 0x04, 0x02]
        regres = bytearray(4)
        with self.device as bus:
            for rctr in range(0, 4):
                bus.write(bytearray([oreg[rctr]]))
                print(oregname[rctr])
                bus.readinto(regres)
                print(regres[0])
                print(regres[0] == signature[rctr])
                time.sleep(0.001)

    def conv_twos_comp(self, b):
        if b & 0x80 << 8:
            b = -1 * ((b ^ 0xffff) + 1)
        return b

    def movement(self):
        x, y = self.update_point()
        x = self.conv_twos_comp(x)
        y = self.conv_twos_comp(y)
        if not x == 0 or not y == 0:
            x, y = self.filter_movement(x, y)
            if pins.layer_2_key.value:
                mouse.move(0, 0, round(-x*0.13), round(-y*0.13))
            else:
                mouse.move(y, x, 0, 0)
            self.is_moving = True
        else:
            self.is_moving = False

    def filter_movement(self, x, y):
        def weight_average_history(history):
            i = -10
            curve = 2
            move_sum = 0
            weight_sum = 0
            for movement in history:
                move_sum = movement * curve ** i + move_sum
                weight_sum = curve ** i + weight_sum
                i = i + 1
            return round(move_sum / weight_sum)
        self.mouse_x_move_history.pop(0)
        self.mouse_x_move_history.append(x)
        self.mouse_y_move_history.pop(0)
        self.mouse_y_move_history.append(y)
        return weight_average_history(self.mouse_x_move_history), weight_average_history(self.mouse_y_move_history)


right_mouse = PMW3389(pins.cs_right)

