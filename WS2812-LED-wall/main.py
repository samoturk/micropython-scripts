import machine
import time

def toggle_pin(p):
    p.value(not p.value())

pin = machine.Pin(2, machine.Pin.OUT)

print('Check if blink works..')
toggle_pin(pin)
time.sleep_ms(500)
toggle_pin(pin)
time.sleep_ms(500)
toggle_pin(pin)
print('Loading the rest..')

# Imports
import machine, neopixel, time
from os import urandom

# Define colors on WS2812 LEDs
colors = {'red':(False,True,False), 'green':(True,False,False), 
          'blue':(False,False,True), 'pink':(False,True,True), 
          'aqua':(True,False,True), 'yellow':(True,True,False),
          'white':(True,True,True)}

# Default intensity
di = 128

# Intensities for WS2812 LEDs. They can go up to 255
intensities = (0, 1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21, 27, 35, 46, 59, 76, 
               99, 128)

def generate_color_intensities(color_tuple, intensities=intensities, reverse=False):
    """ Translates color tuple to list of tuples increasing increasing intensities.
    Useful to fade in or out.    
    """
    return list(zip(*tuple((intensities if x else [0]*len(intensities) for x in color_tuple))))

letter_codes = {'a': 25, 'b': 24, 'c': 23, 'd': 22, 'e': 21, 'f': 20, 'g': 19,
                'h': 18, 'i': 17, 'j': 16, 'k': 15, 'l': 14, 'm': 13, 'n': 12,
                'o': 11, 'p': 10, 'q': 9, 'r': 8, 's': 7, 't': 6, 'u': 5,
                'v': 4, 'w': 3, 'x': 2, 'y': 1, 'z': 0}

def random_colors(n, colors):
    """ Generates a list of n random colors from colors"""
    ints = [int(urandom(1)[0]//(255//(len(colors)-1))) for x in range(n)]
    return [list(colors.keys())[i] for i in ints]

def encode_str(string):
    """ Encodes a string in LED positions if character is in asci letters, !, ?
    and <space> are kept, everything else is ignored.
    """
    sequence = []
    for x in string.lower():
        if x in letter_codes:
            sequence.append(letter_codes[x])
        elif x == '!':
            sequence.append('!')
        elif x == '?':
            sequence.append('!')
        elif x == ' ':
            sequence.append(' ')
    return sequence

def leds_off(np, leds='all'):
    """ Turns off LEDs, by default all. If privided with list of LED positions,
    it will turn off just those.
    """    
    if leds == 'all':    
        leds = range(np.n)
    for led in leds:
        np[led] = (0,0,0)
        np.write()

def leds_on(np, color='random', leds='all'):
    """ Turns LEDs on. Color can be tuple with intensities eg: (128,0,0), or if 
    it is a str from colors, then it will take that or if it is 'random', it will 
    assign a random color to each of the LEDs. If provided with list of LED 
    positions, it will turn on just those. It reads intensity from 'di' variable.
    """
    if leds == 'all':    
        leds = range(np.n)    
    if color in colors:
        color = tuple(di if x else 0 for x in colors[color])     
    if color == 'random':
        cols = [[di if z else 0 for z in colors[x]] for x in 
                                        random_colors(len(leds), colors)]
    else:
        cols = [color]*len(leds)
    leds_off(np, leds=leds)
    for led,c in zip(leds, cols):
        np[led] = c
    np.write()

def leds_fade(np, color, leds='all', fade_out=True, ms=50):
    """ Fades LEDs in. Color has to be in colors. If provided with list of LED 
    positions, it will use just those.
    """
    if leds == 'all':
        leds = range(np.n)
    color_intensities = generate_color_intensities(colors[color])
    if fade_out:
        color_intensities += reversed(color_intensities)
    for i in color_intensities:
        for led in leds:
            np[led] = i
            np.write()
            time.sleep_ms(int(ms))
   
def leds_sequence(np, seq, ms=500, color='white', clear=True, fade=True, **kwargs):
    """ Turns on LEDs in sequence. Sequence should be a list of ints corresponding
    to LED positions. <space>, ! and ? are also allowed and trigger special actions.
    Sequence can be encoded from str by calling encode_str(). If color is 'random' 
    the colors will be assigned randomly.
    """
    leds_off(np)
    if fade:
        led_on_funct = leds_fade
    else:
        led_on_funct = leds_on
    # Assign colors for sequence
    if color == 'random':
        cols = random_colors(len(seq), colors)
    else:
        cols = [color]*len(seq)
    for s,c in zip(seq, cols):
        if s == ' ':
            leds_off(np)
            time.sleep_ms(int(ms)*2)
        elif s == '!':
            leds_on(np)
            time.sleep_ms(int(ms))
            leds_off(np)
            time.sleep_ms(int(ms))
            leds_on(np)
            time.sleep_ms(int(ms))
            leds_off(np)
            time.sleep_ms(int(ms))
            leds_on(np)
            time.sleep_ms(int(ms))
            leds_off(np)
            time.sleep_ms(int(ms))
        elif s == '?':
            leds_off(np)
            time.sleep_ms(int(ms)*2)
        else:
            led_on_funct(np, leds=[s], color=c, **kwargs)
            time.sleep_ms(int(ms))
            if clear:
                leds_off(np, leds=[s])

        
def tests(np, delay=250):
    print('Starting tests..')
    time.sleep_ms(delay)
    print('Turn on leds 0 and 2 with red color')
    time.sleep_ms(delay)
    leds_on(np, color='red', leds=[0,2])
    print('Turn off led 0')    
    time.sleep_ms(delay)
    leds_off(np, leds=[0])
    print('Turn off all')    
    time.sleep_ms(delay)
    leds_off(np)
    print('Turn on all, random colors')
    time.sleep_ms(delay)
    leds_on(np, color='random', leds='all')
    leds_off(np)
    print('Fade in and out leds 0 and 2 with white color')
    time.sleep_ms(delay)
    leds_fade(np, 'white', leds=[0,2], fade_out=True, ms=50)
    print('Run a sequence "abcdefghijklmnopqrstuvwxyz !" with random colors')
    time.sleep_ms(delay)
    leds_sequence(np, encode_str('abcdefghijklmnopqrstuvwxyz !'), color='random')
    print('Run a sequence "abcdefghijklmnopqrstuvwxyz !" with random colors, not fadeout')    
    time.sleep_ms(delay)
    leds_sequence(np, encode_str('abcdefghijklmnopqrstuvwxyz !'), color='random', clear=False, fade_out=False)

np = neopixel.NeoPixel(machine.Pin(15), 26)
leds_sequence(np, encode_str('run !!!'), color='random')
leds_sequence(np, encode_str('abcdefghijklmnopqrstuvwxyz !'), color='random', clear=False, fade_out=False, ms=1)
leds_sequence(np, encode_str('abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba'), color='random', clear=False, fade=False, ms=100)
#leds_sequence(np, encode_str('abcd !'), color='random', clear=False, fade_out=False)
leds_sequence(np, encode_str('riajskbltlclumdmvnenwnfoxpgpyphqz riajskbltlclumdmvnenwnfoxpgpyphqz '), color='random', clear=True, fade=False, ms=10)
leds_sequence(np, encode_str('abcdefghijklmnopqrstuvwxyz zyxwvutsrqponmlkjihgfedcba '), color='random', clear=False, fade=False, ms=10)