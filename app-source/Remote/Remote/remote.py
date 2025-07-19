"""A simple app to query Wikipedia for page summaries."""
import requests, network, time, json
from machine import Pin, freq
from lib.display import Display
from lib.userinput import UserInput
from lib.hydra.config import Config
from lib.device import Device
from lib.hydra.popup import UIOverlay
from font import vga1_8x16 as font

# ~~~~~~~~~~~~~~~~~~~~~~~~~ global objects/vars ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
DISPLAY_HEIGHT_HALF = DISPLAY_HEIGHT // 2

MAX_H_CHARS = DISPLAY_WIDTH // 8
MAX_V_LINES = DISPLAY_HEIGHT // 16


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Function Definitions: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def gprint(text, clr_idx=8):
    text = str(text)
    print(text)
    tft.fill(config.palette[2])
    x = DISPLAY_WIDTH_HALF - (len(text) * 4)
    tft.text(text, x, DISPLAY_HEIGHT_HALF, config.palette[clr_idx], font=font)
    tft.show()


    # class Roku:
    #     def __init__(self, ip):
    #         self.base_url = f"http://{ip}:8060"
    #         self.requests = urequests

    #     def keypress(self, key):
    #         url = f"{self.base_url}/keypress/{key}"
    #         try:
    #             resp = self.requests.post(url)
    #             resp.close()
    #             return True
    #         except Exception as e:
    #             print("[ERROR] Failed to send keypress:", key, e)
    #             return False



# ~~~~~~~~~~~~~~~~~~~~~~~~~ Utility Functions ~~~~~~~~~~~~~~~~~~~~~~~
def gprint(text, clr_idx=8):
    text = str(text)
    print(text)
    tft.fill(config.palette[2])
    x = DISPLAY_WIDTH_HALF - (len(text) * 4)
    tft.text(text, x, DISPLAY_HEIGHT_HALF, config.palette[clr_idx], font=font)
    tft.show()

def errprint(text):
    text = str(text)
    print(text)
    tft.fill(config.palette[1])
    OVERLAY.error(text)


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Main Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


gprint('Connecting to WIFI...', clr_idx=6)
time.sleep_ms(1000)

# turn on wifi if it isn't already
if not nic.active():
    nic.active(True)

# keep trying to connect until command works
while True:
    try:
        nic.connect(config['wifi_ssid'], config['wifi_pass'])
        break
    except Exception as e:
        gprint(f"Got this error while connecting: {repr(e)}", clr_idx=11)

# wait until connected
gprint(f"Waiting for connection...")
while not nic.isconnected():
    time.sleep_ms(100)

gprint("Wifi connected", clr_idx=4)

ROKU_IP = "192.168.68.49"

def create_keypress(key):
    url = f"http://{ROKU_IP}:8060/keypress/{key}"
    requests.post(url)


# roku = Roku(ROKU_IP)

# gprint("Roku init", clr_idx=4)

# current_text = "Ready"

while True:
    keys = kb.get_new_keys()
    kb.ext_dir_keys(keys)

    if keys:
        # current_text = str(keys)
        # gprint(current_text, clr_idx=6)       

        # Roku key mappings
        if "UP" in keys:
            create_keypress("Up")
        elif "DOWN" in keys:
            create_keypress("Down")
        elif "LEFT" in keys:
            create_keypress("Left")
        elif "RIGHT" in keys:
            create_keypress("Right")
        elif "A" in keys:
            create_keypress("Home")
        elif "B" in keys:
            create_keypress("Back")
        elif "ENTER" in keys:
            create_keypress("Select")
        elif "ESC" in keys:
            create_keypress("Back")
        elif "SPACE" in keys:
            create_keypress("Play")


    time.sleep_ms(10)

