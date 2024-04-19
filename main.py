import pydirectinput
import time
import random
from PIL import Image
from pynput import keyboard
import sys
import easygui

exiting = False
paused = True
base_pos = 0

def on_press(key):
    if key == keyboard.Key.esc:
        global exiting
        exiting = True
        sys.exit(0)

    if key == keyboard.Key.f1:
        global paused
        paused = not paused

    if key == keyboard.Key.f3:
        global start_pos
        start_pos = list(pydirectinput.position())
        easygui.msgbox("Start Pos set to " + str(start_pos), "Spray Printer")

    if key == keyboard.Key.f4:
        global base_pos
        base_pos = pydirectinput.position()[0]

    if key == keyboard.Key.f5:
        global step_size
        step_size = abs(pydirectinput.position()[0] - base_pos)
        easygui.msgbox("Step Size set to " + str(step_size), "Spray Printer")

    if key == keyboard.Key.f6:
        global hex_picker
        hex_picker = pydirectinput.position()
        easygui.msgbox("Hex Picker set to " + str(hex_picker), "Spray Printer")

    if key == keyboard.Key.f7:
        global speed
        sp_temp = easygui.enterbox(msg="Enter your speed greater than 0 (higher is slower, default is 0.025", title="Spray Printer")
        speed = float(sp_temp)
        easygui.msgbox("Speed set to " + str(speed), "Spray Printer")

def check_paused():
    while paused:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

# Definitions
hex_picker = [243, 1017]
start_pos = [599, 101]
step_size = 6
speed = 0.025

filename = easygui.fileopenbox()

img = Image.open(filename)
#img = img.convert("RGBA")

easygui.msgbox(msg="""(Before Printing)
Press F6 to show Spray Printer where your hex picker is.
Press F7 to choose your speed.

(Printing)
Press F3 to set the start position.
Turn on Cursor Preview, then place a pixel and press F4.
Move over one pixel's worth, then press F5. Erase those two pixels.
Unequip the spray can.
Press F1 to begin printing.
(F1 can also be used to pause!)""",
                  title="Spray Printer")

check_paused()
pydirectinput.press("1")
pydirectinput.moveTo(start_pos[0], start_pos[1], speed * 5)

startTime = time.time()

colors = img.getcolors(maxcolors=0xFFFF)

for color in colors:
    if color[1][3] == 0:
        continue

    hexcode = '%02x%02x%02x%02x' % color[1]
    hexcode = hexcode[0:6].upper()

    # set the color

    print(f"{hexcode}: {color[0]} pixels | {colors.index(color) + 1} / {len(colors) - 1}")

    check_paused()

    pydirectinput.moveTo(hex_picker[0], hex_picker[1], speed * 10)
    time.sleep(speed * 3)
    pydirectinput.mouseDown()
    time.sleep(speed * 5)
    pydirectinput.mouseUp()
    check_paused()
    time.sleep(speed * 3)
    pydirectinput.typewrite(hexcode + "\n", speed * 1.5)
    check_paused()
    
    for r in range(5):
        pydirectinput.press("enter")
        time.sleep(speed)

    check_paused()
    time.sleep(speed * 20)
    check_paused()

    for y in range(img.height):
        for x in range(img.width):
            check_paused()
            if exiting:
                sys.exit(0)
                
            if img.getpixel((x, y)) == color[1]:
                pydirectinput.moveTo(start_pos[0] + (step_size * x), start_pos[1] + (step_size * y), speed)

                pydirectinput.mouseDown()
                time.sleep(speed * 3)
                pydirectinput.mouseUp()
                time.sleep(speed * 3)

    pydirectinput.moveTo(start_pos[0], start_pos[1], speed * 10)

timer = f"Finished in {round(time.time() - startTime, 3)} seconds"
easygui.msgbox(timer, "Spray Painter")
