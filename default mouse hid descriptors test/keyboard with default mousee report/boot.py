import usb_hid

# mouse specific descriptors out of keymouse right
MOUSE_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,                    # USAGE_PAGE (Generic Desktop)
    0x09, 0x02, # USAGE(Mouse)
    0xa1, 0x01, # COLLECTION(Application)
    0x09, 0x01, # USAGE(Pointer)
    0xA1, 0x00, # COLLECTION(Physical)
    0x05, 0x09, # USAGE_PAGE(Button)
    0x19, 0x01, # USAGE_MINIMUM
    0x29, 0x03, # USAGE_MAXIMUM
    0x15, 0x00, # LOGICAL_MINIMUM(0)
    0x25, 0x01, # LOGICAL_MAXIMUM(1)
    0x95, 0x03, # REPORT_COUNT(3)
    0x75, 0x01, # REPORT_SIZE(1)
    0x81, 0x02, # INPUT(Data, Var, Abs)
    0x95, 0x01, # REPORT_COUNT(1)
    0x75, 0x05, # REPORT_SIZE(5)
    0x81, 0x03, # INPUT(Const, Var, Abs)
    0x05, 0x01, # USAGE_PAGE(Generic Desktop)
    0x09, 0x30, # USAGE(X)
    0x09, 0x31, # USAGE(Y)
    0x09, 0x38, # USAGE(Wheel)
    0x15, 0x81, # LOGICAL_MINIMUM(-127)
    0x25, 0x7F, # LOGICAL_MAXIMUM(127)
    0x75, 0x08, # REPORT_SIZE(8)
    0x95, 0x03, # REPORT_COUNT(3)
    0x81, 0x06, # INPUT(Data, Var, Rel)
    0xC0,        # End Collection
    0xC0,        # End Collection

    #......................... Horizontal Wheel
    #0x05, 0x0C,  # Usage Page (Consumer)
    #0x0A, 0x38, 0x02,  # Usage (AC Pan)
    #0x15, 0x81,  # Logical Minimum (-127)
    #0x25, 0x7F,  # Logical Maximum (127)
    #0x75, 0x08,  # Report Size (8)
    #0x95, 0x01,   # Report Count (1)
    #0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
))

mouse2 = usb_hid.Device(
    report_descriptor=MOUSE_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x02,                # Mouse
    report_ids=(2,),           # Descriptor uses report ID 2.
    in_report_lengths=(4,),    # This mouse sends 4 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.CONSUMER_CONTROL,
     mouse2)
)

print('boot successful')