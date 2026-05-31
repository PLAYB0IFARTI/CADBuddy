import digitalio
import board

class Button:
    def __init__(self, pin, pullDown=True):
        # Create DigitalInOut object
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pv = False # previous value
        self.toggle = True

        # CircuitPython uses Pull.UP or Pull.DOWN
        if pullDown:
            self.pin.pull = digitalio.Pull.DOWN
        else:
            self.pin.pull = digitalio.Pull.UP

        self.pd = pullDown

    def is_pressed(self):
        if self.pd:
            return self.pin.value == True
        else:
            return self.pin.value == False

    def pressed(self):
        return self.is_pressed()
    
    # if you just wanna check if its pressed and do one action
    
    def just_pressed(self):
        current = self.is_pressed()

        if current and not self.pv:
            self.pv = current
            return True
        else:
            self.pv = current
            return False
    
    # toggle on and off
    
    def toggled(self):
        if not self.toggle:
            self.toggle = True
            return self.pin.value == True
        else:
            self.toggle = False
            return self.pin.value == False
        
            

