from microbit import pin0, display, Image
import music

pin0.is_touched()

pin0.write_digital(1)

music.play(music.BA_DING)
