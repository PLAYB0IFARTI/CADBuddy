# general use imports
import time
import digitalio
import board
import analogio
import usb_hid
# oled display

import busio
import displayio
import terminalio
import i2cdisplaybus
import adafruit_displayio_sh1106

# shapes and stuff
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label

# keyboard functions

from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# controls computer

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# custom classes

from joystick import Joystick
from button import Button


# -----------------------------------------------------------------------------------

# constants
# for gpio pins, USE board.GP{pin number}, eg board.GP5

WIDTH = 128
HEIGHT = 64

# all oled stuff
hotkeys = [
    "EXT", "FLT", "SKC",
    "ACC", "NRM", "ROT",
    "ESC",   "CPY",   "PST"
]



# grid settings
col_w = 42
row_h = 20
start_x = 2
start_y = 10

cell = 21  # square size
pad = 2    # text padding inside cell

# -----------------------------------------------------------------------------------

# funky functions for the oled

# displays every hotkey
def display_hotkeys():
    g = displayio.Group()
    for i, key in enumerate(hotkeys):
        row = i // 3
        col = i % 3
        x = col * cell
        y = row * cell

        box = Rect(x, y, cell - 1, cell - 1, fill=None, outline=0xFFFFFF)
        g.append(box)

        t = label.Label(terminalio.FONT, text=key, color=0xFFFFFF, x=x + pad, y=y + (cell // 2))
        g.append(t)
    splash.append(g)

# displays the keys with the rotate symbol
def display_rotate():
    circle = Circle(95,28,15,fill = None,outline = 0xFFFFFF)
    lines = []
    lines.append(Line(88,20,88,9,color = 0x000000))
    lines.append(Line(89,20,89,9,color = 0x000000))
    lines.append(Line(90,20,90,9,color = 0x000000))
    lines.append(Line(91,20,91,9,color = 0x000000))
    lines.append(Line(92,20,92,9,color = 0x000000))
    lines.append(Line(93,20,93,9,color = 0x000000))
    lines.append(Line(94,20,94,9,color = 0x000000))
    
    # arrow line
    lines.append(Line(95,13,101,6,color = 0xFFFFFF))
    lines.append(Line(95,13,99,21,color = 0xFFFFFF))
    
    g = displayio.Group()
    g.append(circle)
    for l in lines:
        g.append(l)
    splash.append(g)
    
# displays the keys with the pan symbol
def display_pan():
    g = displayio.Group()
    
    lines = []
    lines.append(Line(95,28,95,12,color = 0xFFFFFF))
    lines.append(Line(95,12,90,17,color = 0xFFFFFF))
    lines.append(Line(95,12,100,17,color = 0xFFFFFF))
    
    lines.append(Line(95,28,80,28,color = 0xFFFFFF))
    lines.append(Line(80,28,85,34,color = 0xFFFFFF))
    lines.append(Line(80,28,85,22,color = 0xFFFFFF))
    
    lines.append(Line(95,28,110,28,color = 0xFFFFFF))
    lines.append(Line(110,28,105,34,color = 0xFFFFFF))
    lines.append(Line(110,28,105,22,color = 0xFFFFFF))
    
    lines.append(Line(95,28,95,43,color = 0xFFFFFF))
    lines.append(Line(95,43,90,37,color = 0xFFFFFF))
    lines.append(Line(95,43,100,37,color = 0xFFFFFF))
    
    for l in lines:
        g.append(l)
    splash.append(g)

def get_text_area(msg,xpos,ypos):
    text_area = label.Label(terminalio.FONT, text = msg, color = 0xFFFFFF, x = xpos, y = ypos)
    return text_area

def display_stabilized(stab_mode):
    if stab_mode:
        splash.append(get_text_area("STB=ON",80,50))
        
    else:
        splash.append(get_text_area("STB=OFF",80,50))


# -----------------------------------------------------------------------------------

# declaring sum stuff like buttons

BUTTON_1 = Button(board.GP9)
BUTTON_2 = Button(board.GP16)
BUTTON_3 = Button(board.GP17)
BUTTON_4 = Button(board.GP12)
BUTTON_5 = Button(board.GP11)
BUTTON_6 = Button(board.GP10)
BUTTON_7 = Button(board.GP15)
BUTTON_8 = Button(board.GP14)
BUTTON_9 = Button(board.GP13)

# volume control stuff

pot = analogio.AnalogIn(board.GP26)
cc = ConsumerControl(usb_hid.devices)
last_value = pot.value

# joystick stuff

X_pin = analogio.AnalogIn(board.GP27)
Y_pin = analogio.AnalogIn(board.GP28)
BUTTON_JS = Button(board.GP22, pullDown=False) #button press for joystick
Sticks = Joystick(X_pin, Y_pin)

# keyboard stuff

kbd = Keyboard(usb_hid.devices)

# mouse stuff

mouse = Mouse(usb_hid.devices)

# oled stuff

displayio.release_displays()

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=128, height=64)

splash = displayio.Group()
display.root_group = splash

text_area = label.Label(terminalio.FONT, text="Hello!", color=0xFFFFFF, x=10, y=30)

count = 0

display_hotkeys()
display_rotate()
display_stabilized(True)


# -----------------------------------------------------------------------------------

print("hello world")

blist = [BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4, BUTTON_5, BUTTON_6, BUTTON_7, BUTTON_8,BUTTON_9]



pan_mode = False
prev_mode = False

prev_js_move = False
prev_js_held = False

stab_mode = True
prev_stab_mode = True

frame_count = 0

idx_for_icon = 1
idx_for_stab = 2
while True:
    try:
        time.sleep(0.020) # 20 fps
        #print(Sticks.get_x())
        #print(Sticks.get_y())
        #print(BUTTON_1.pin.value)
        #print(BUTTON_1.pv)
        # print(BUTTON_1.pv)
# -----------------------------------------------------------------------------------
        # Button stuff
        
        if BUTTON_1.just_pressed():
            kbd.send(Keycode.LEFT_SHIFT, Keycode.E)
            #print(BUTTON_1.pin.value)
            
        if BUTTON_2.just_pressed():
            kbd.send(Keycode.LEFT_SHIFT, Keycode.F)
            
        if BUTTON_3.just_pressed():
            kbd.send(Keycode.LEFT_SHIFT, Keycode.S)
        
        if BUTTON_4.just_pressed():
            kbd.send(Keycode.ENTER)
        
        if BUTTON_5.just_pressed():
            kbd.send(Keycode.N)
        
        if BUTTON_6.just_pressed():
            BUTTON_6.toggled()
            stab_mode = not stab_mode
        
        if BUTTON_7.just_pressed():
            kbd.send(Keycode.ESCAPE)
        
        if BUTTON_8.just_pressed():
            kbd.send(Keycode.CONTROL, Keycode.C)
        
        if BUTTON_9.just_pressed():
            kbd.send(Keycode.CONTROL, Keycode.V)
            
            
            
        
# -----------------------------------------------------------------------------------
        # mouse stuff
        
        # change in mouse pos
        
        cg_x = x=int((-(Sticks.get_x()) + 50) // -10)
        cg_y = x=int((-(Sticks.get_y()) + 50) // -10)
        
        # mouse states
        
        ms_x = cg_x != 0
        ms_y = cg_y != 0
        ms_both = ms_x or ms_y
        js_moving = ms_both
        
        # Make joystick hold either alt or right click when the joystick *starts* moving
        if js_moving and js_moving != prev_js_move: #if the joystick just started moving
            if not BUTTON_6.pin.value: 
                kbd.press(Keycode.ALT)
            if pan_mode:
                mouse.press(Mouse.MIDDLE_BUTTON)
            else:
                mouse.press(Mouse.RIGHT_BUTTON)
        if not js_moving and  js_moving != prev_js_move: # if the joystick JUST stopped
            if not BUTTON_6.pin.value:
                kbd.release(Keycode.ALT)
            if pan_mode:
                mouse.release(Mouse.MIDDLE_BUTTON)
            else:
                mouse.release(Mouse.RIGHT_BUTTON)
        if BUTTON_JS.just_pressed():
            pan_mode = not pan_mode
        
        prev_js_move = js_moving
        
        if js_moving:
            mouse.move(x = -cg_x, y = cg_y)
                
# -----------------------------------------------------------------------------------
        #potentiometer stuff
        current = pot.value

        if current > last_value + 1000:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)


        elif current < last_value - 1000:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)


        last_value = current

# -----------------------------------------------------------------------------------
        if BUTTON_6.toggle and ms_both:
            kbd.press(Keycode.ALT)
        else:
            kbd.release(Keycode.ALT)
        
    except Exception as e:
        print(e)
        
# ----------------- OLED HANDLING ----------------------------------
    if pan_mode != prev_mode: # if a change in pan mode occurred
        prev_mode = pan_mode # updating previous mode
        if (pan_mode): #if its panning
        
            while (len(splash) > 1):
                splash.pop()
            display_pan()
            display_stabilized(stab_mode)
        else: 
            while(len(splash) > 1):
                splash.pop()
            display_rotate()
            display_stabilized(stab_mode)
    if stab_mode != prev_stab_mode:
        prev_stab_mode = stab_mode
        display_stabilized(stab_mode)
        splash.pop(2)


