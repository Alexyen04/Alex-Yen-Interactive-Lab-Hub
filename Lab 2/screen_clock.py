import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep

from button_controls import button_a_pressed, button_b_pressed, create_time_screen, create_weather_screen
from weather import get_current_temperature

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.D5) 
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# MY PART 2
# while True:
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0, 0, width, height), outline=0, fill=400)

#     #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    
#  
#     # y = top
#     # curr_time = strftime("%m/%d/%Y %H:%M:%S")

#     # draw.text((x,y), curr_time, font=font, fill="#FFFFFF")
    

while True:
    if button_a_pressed():
        frame = create_time_screen(width, height)
    elif button_b_pressed():
        temperature = get_current_temperature()
        frame = create_weather_screen(width, height, temperature)
    else:
        frame = Image.new(
            "RGB",
            (width, height),
            (100, 150, 220)
        )

    disp.image(frame, rotation)
    time.sleep(0.05)

# images = [
#     "images/dawn.png",
#     "images/morning.png",
#     "images/midday.png",
#     "images/afternoon.png",
#     "images/dusk.png",
#     "images/night.png",
# ]

# while True:
#     for image in images:
#         test_image = Image.open(image).convert("RGB")
#         test_image = test_image.resize((240,135))

#         # Display image.
#         disp.image(test_image, rotation)
#         time.sleep(2)
