import usb_hid

# mouse specific descriptors out of keymouse right
MOUSE_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x02,  # Usage (Mouse)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x06,  # Report ID (6)
    0x09, 0x01,  # Usage (Pointer)
    0xA1, 0x00,  # Collection (Physical)
    0x05, 0x09,  # Usage Page (Button)
    0x19, 0x01,  # Usage Minimum (0x01)
    0x29, 0x03,  # Usage Maximum (0x03)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x35, 0x00,  # Physical Minimum (0)
    0x45, 0x01,  # Physical Maximum (1)
    0x65, 0x00,  # Unit (None)
    0x55, 0x00,  # Unit Exponent (0)
    0x75, 0x01,  # Report Size (1)
    0x95, 0x03,  # Report Count (3)
    0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95, 0x05,  # Report Count (5)
    0x81, 0x03,  # Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x30,  # Usage (X)
    0x26, 0xFF, 0x07,  # Logical Maximum (2047)
    0x45, 0x00,  # Physical Maximum (0)
    0x75, 0x0C,  # Report Size (12)
    0x95, 0x01,  # Report Count (1)
    0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0x09, 0x31,  # Usage (Y)
    0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0x09, 0x38,  # Usage (Wheel)
    0x25, 0x7F,  # Logical Maximum (127)
    0x75, 0x08,  # Report Size (8)
    0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x0C,  # Usage Page (Consumer)
    0x0A, 0x38, 0x02,  # Usage (AC Pan)
    0x81, 0x06,  # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    0xC1, 0x00,  # End Collection
    0xC1, 0x00,  # End Collection
))

mouse2 = usb_hid.Device(
    report_descriptor=MOUSE_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x02,                # Mouse
    report_ids=(6,),           # Descriptor uses report ID 6.
    in_report_lengths=(5,),    # This mouse sends 5 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.CONSUMER_CONTROL,
     mouse2)
)
