# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import digitalio
import board
from PIL import Image, ImageDraw
import math
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import
from time import sleep
from datetime import datetime

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
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
    rotation=90
)
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

DAY_BG = "images/daytimeNYCskyline.jpeg"
NIGHT_BG = "images/nighttimeNYCskyline.jpeg"
SUN_SPRITE = "images/sunsprite.webp"
MOON_SPRITE = "images/moonsprite.gif"

SPRITE_WIDTH = 56
SOLAR_START_HOUR = 7    # sun rises (leftmost) at 7am
SOLAR_END_HOUR = 19     # sun sets (rightmost); night picture starts at 7pm
LUNAR_START_HOUR = 19   # moon rises (leftmost) when night falls at 7pm
LUNAR_END_HOUR = 6      # moon sets (rightmost) at 6am


def load_background(input):
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    image = Image.open(input)
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    return image.convert("RGB")


def load_sprite(path, target_width):
    image = Image.open(path).convert("RGBA")
    scaled_height = round(image.height * target_width / image.width)
    return image.resize((target_width, scaled_height), Image.BICUBIC)


def sprite_position(t, sprite):
    # t travels 0 (left, mid-height) -> 0.5 (center, top) -> 1 (right, mid-height)
    sw, sh = sprite.size
    left = 0  # centered on the left edge, half the sprite cut off
    right = width  # centered on the right edge, half the sprite cut off
    mid = height // 2  # start/end at the vertical middle of the picture
    amp = (height - sh) // 2  # arc top stays just on screen
    x = left + t * (right - left)
    y = mid - math.sin(math.pi * t) * amp
    return int(x), int(y)


def paste_sprite(frame, sprite, cx, cy):
    sw, sh = sprite.size
    x = int(cx - sw / 2)
    y = int(cy - sh / 2)
    frame.paste(sprite, (x, y), sprite)


day_bg = load_background(DAY_BG)
night_bg = load_background(NIGHT_BG)
sun_sprite = load_sprite(SUN_SPRITE, SPRITE_WIDTH)
moon_sprite = load_sprite(MOON_SPRITE, SPRITE_WIDTH)

temp_time = 7
# Display image.
while True:
    # if temp_time == 25:
    #     temp_time = 1
    # else:
    #     temp_time += 1
    # hour = temp_time
    
    hour = datetime.now().hour

    if SOLAR_START_HOUR <= hour < SOLAR_END_HOUR:
        # Daytime sky with the sun, one step per hour from 7am-7pm.
        frame = day_bg.copy()
        t = (hour - SOLAR_START_HOUR) / (SOLAR_END_HOUR - SOLAR_START_HOUR)
        paste_sprite(frame, sun_sprite, *sprite_position(t, sun_sprite))
    else:
        # Nighttime sky with the moon, one step per hour from 7pm-6am.
        frame = night_bg.copy()
        if hour >= LUNAR_START_HOUR or hour <= LUNAR_END_HOUR:
            p = (hour - LUNAR_START_HOUR) % 24
            t = p / ((LUNAR_END_HOUR - LUNAR_START_HOUR) % 24)
            paste_sprite(frame, moon_sprite, *sprite_position(t, moon_sprite))

    disp.image(frame)
    sleep(1)