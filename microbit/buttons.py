from microbit import running_time, button_a, button_b, display

while running_time() < 10000:
    if button_a.is_pressed():
        display.show("A")
    elif button_b.is_pressed():
        display.show("B")
    else:
        display.show("-")
display.clear()
