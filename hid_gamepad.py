import usb_hid

GAMEPAD_REPORT_DESCRIPTOR = bytes([
    0x05, 0x01,        # Usage Page: Generic Desktop
    0x09, 0x05,        # Usage: Gamepad
    0xA1, 0x01,        # Collection: Application
    0x85, 0x04,        #   Report ID: 4
    0x09, 0x30,        #   Usage: X
    0x09, 0x31,        #   Usage: Y
    0x15, 0x81,        #   Logical Min: -127
    0x25, 0x7F,        #   Logical Max: 127
    0x75, 0x08,        #   Report Size: 8
    0x95, 0x02,        #   Report Count: 2
    0x81, 0x02,        #   Input: Data, Variable, Absolute
    0xC0,              # End Collection
])

gamepad_device = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,
    usage=0x05,
    report_ids=(4,),
    in_report_lengths=(2,),
    out_report_lengths=(0,),
)

class Gamepad:
    def __init__(self, devices):
        self._device = None
        for d in devices:
            if d.usage_page == 0x01 and d.usage == 0x05:
                self._device = d
                break
        if self._device is None:
            raise ValueError("Gamepad not found - power cycle after saving boot.py?")

    def move_joysticks(self, x=0, y=0):
        import time
        for _ in range(10):
            try:
                self._device.send_report(bytes([x & 0xFF, y & 0xFF]), report_id=4)
                return
            except OSError:
                time.sleep(0.1)
        raise OSError("USB busy")