from microbit import *

while running_time() < 1000:
    display.show(Image.ASLEEP)

display.show(Image.SURPRISED)

while True:
    if button_a.is_pressed():
        display.show(Image.HAPPY)
    elif button_b.is_pressed():
        break
    else:
        display.show(Image.SAD)

display.clear()

while True:
    reading = accelerometer.get_x()
    if reading > 20:
        display.show(">")
    elif reading < -20:
        display.show("<")
    else:
        display.show("-")
