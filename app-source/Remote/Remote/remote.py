"""
Roku Remote for MicroHydra

Control a Roku device over Wi-Fi using MicroPython.
"""

import time, network, urequests
from machine import freq
from lib.display import Display
from lib.userinput import UserInput
from lib.hydra.config import Config
from lib.device import Device
from font import vga1_8x16 as font
from lib.hydra.popup import UIOverlay


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Setup & Globals ~~~~~~~~~~~~~~~~~~~~~~~~~
freq(240000000)

if "CARDPUTER" in Device:
    import neopixel
    led = neopixel.NeoPixel(Pin(21), 1, bpp=3)

tft = Display(use_tiny_buf=("spi_ram" not in Device))
config = Config()
kb = UserInput()
nic = network.WLAN(network.STA_IF)
OVERLAY = UIOverlay()

DISPLAY_WIDTH = Device.display_width
DISPLAY_HEIGHT = Device.display_height
DISPLAY_WIDTH_HALF = DISPLAY_WIDTH // 2

_CHAR_WIDTH = 8
_CHAR_WIDTH_HALF = _CHAR_WIDTH // 2

ROKU_IP = "192.168.1.100"  # <-- Set your Roku's IP here
ROKU_URL = f"http://{ROKU_IP}:8060"


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions ~~~~~~~~~~~~~~~~~~~~~~~
def gprint(text, clr_idx=8):
    text = str(text)
    print(text)
    tft.fill(config.palette[2])
    x = DISPLAY_WIDTH_HALF - (len(text) * _CHAR_WIDTH_HALF)
    tft.text(text, x, DISPLAY_HEIGHT // 2, config.palette[clr_idx], font=font)
    tft.show()

def errprint(text):
    text = str(text)
    print("[ERROR]", text)
    tft.fill(config.palette[1])
    OVERLAY.error(text)

def connect_wifi():
    gprint("Connecting Wi-Fi...", clr_idx=6)
    if not nic.active():
        nic.active(True)

    while not nic.isconnected():
        try:
            nic.connect(config['wifi_ssid'], config['wifi_pass'])
        except Exception as e:
            gprint(f"WiFi error: {repr(e)}", clr_idx=11)
            time.sleep(1)
        time.sleep_ms(500)

    gprint("Connected!", clr_idx=4)
    time.sleep(0.5)

def roku_keypress(key):
    try:
        response = urequests.post(f"{ROKU_URL}/keypress/{key}")
        response.close()
        gprint(f"Sent: {key}", clr_idx=5)
    except Exception as e:
        errprint(f"Send failed: {key}\n{e}")
        time.sleep(1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Main Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    connect_wifi()
    gprint("Roku Remote Ready", clr_idx=4)
    time.sleep(1)

    current_text = "Ready"

    while True:
        keys = kb.get_new_keys()
        kb.ext_dir_keys(keys)

        if keys:
            current_text = str(keys)
            gprint(current_text, clr_idx=6)

            # Roku key mappings
            if "UP" in keys:
                roku_keypress("Up")
            elif "DOWN" in keys:
                roku_keypress("Down")
            elif "LEFT" in keys:
                roku_keypress("Left")
            elif "RIGHT" in keys:
                roku_keypress("Right")
            elif "A" in keys:
                roku_keypress("Home")
            elif "B" in keys:
                roku_keypress("Back")
            elif "ENTER" in keys:
                roku_keypress("Select")
            elif "ESC" in keys:
                roku_keypress("Back")
            elif "SPACE" in keys:
                roku_keypress("Play")

        time.sleep_ms(10)


main()
