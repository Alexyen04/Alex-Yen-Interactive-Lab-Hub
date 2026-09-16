import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont

# Button A config
button_A = digitalio.DigitalInOut(board.D23)
button_A.switch_to_input(pull=digitalio.Pull.UP)

# Button B config
button_B = digitalio.DigitalInOut(board.D24)
button_B.switch_to_input(pull=digitalio.Pull.UP)

time_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42)
date_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

weather_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

def button_a_pressed():
    if button_A.value == False: # False = not pressed, True = pressed
        return True

def button_b_pressed():
    if button_B.value == False:
        return True

def create_time_screen(width, height):
    frame = Image.new("RGB", (width, height), (0,0,0))
    draw = ImageDraw.Draw(frame)

    current_date = time.strftime("%b %d, %Y")
    current_time = time.strftime("%I:%M %p")

    date_bbox = draw.textbbox((0, 0), current_date, font=date_font)
    date_width = date_bbox[2] - date_bbox[0]

    time_bbox = draw.textbbox((0, 0), current_time, font=time_font)
    time_width = time_bbox[2] - time_bbox[0]

    date_x = (width - date_width) // 2
    time_x = (width - time_width) // 2

    draw.text(
        (date_x, 25),
        current_date,
        font=date_font,
        fill=(255, 255, 255)
    )

    draw.text(
        (time_x, 55),
        current_time,
        font=time_font,
        fill=(255, 255, 255)
    )

    return frame


def create_weather_screen(width, height, temperature):
    frame = Image.new("RGB", (width, height), (0,0,0))
    draw = ImageDraw.Draw(frame)

    label = "Weather"
    temperature_text = f"{temperature}°F"

    label_bbox = draw.textbbox((0, 0), label, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    label_x = (width - label_width) // 2

    temp_bbox = draw.textbbox((0, 0), temperature_text, font=weather_font)
    temp_width = temp_bbox[2] - temp_bbox[0]
    temp_x = (width - temp_width) // 2

    draw.text(
        (label_x, 20),
        label,
        font=label_font,
        fill=(255, 255, 255)
    )

    draw.text(
        (temp_x, 50),
        temperature_text,
        font=weather_font,
        fill=(255, 255, 255)
    )

    return frame


