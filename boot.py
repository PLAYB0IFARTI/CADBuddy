import usb_hid
#from hid_gamepad import gamepad_device

#usb_hid.enable((usb_hid.Device.KEYBOARD, gamepad_device))

usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL
    )
)