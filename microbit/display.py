from microbit import display
display.scroll("Hello, World!")

# Images
from microbit import display, Image
display.show(Image.HAPPY)


boat = Image("00710:00755:00700:99999:09990")
display.show(boat)

# Animation
display.show(reversed([str(x) for x in range(10)]), loop=False, delay=500)


display.show(Image.ALL_CLOCKS, loop=True, delay=100)

display.clear()
