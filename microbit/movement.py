#from microbit import accelerometer, sleep, display, Image
#
#while True:
#    sleep(100)
#    print("x: {:04d}, y: {:04d}, z {:04d}".format(accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z(
#    )), end="\r")


from microbit import accelerometer, sleep, display, Image

while True:
    sleep(100)
    gesture = accelerometer.current_gesture()
    if gesture == "shake":
        display.show(Image.ANGRY)
    else:
        display.clear()
