"""A simple app to query Wikipedia for page summaries."""
import requests, network, time, json
from machine import Pin, freq
from lib.display import Display
from lib.userinput import UserInput
from lib.hydra.config import Config
from lib.device import Device
from lib.hydra.popup import UIOverlay
from font import vga1_8x16 as font

import socket
import ure


def find_roku_ip():
    subnet = nic.ifconfig()[0].rsplit('.', 1)[0]  # '192.168.1'
    tft.fill(config.palette[6])
    tft.text("Searching for Roku...", 10, DISPLAY_HEIGHT_HALF, config.palette[8], font=font)
    tft.show()
    for last in range(1, 255):
        ip = "%s.%d" % (subnet, last)
        try:
            s = socket.socket()
            s.connect((ip, 8060))
            req = "GET /query/device-info HTTP/1.1\r\nHost: %s\r\n\r\n" % ip
            s.send(bytes(req, 'utf8'))
            data = s.recv(256)
            s.close()
            if b"roku" in data.lower() or b"device-info" in data.lower():
                return ip
        except Exception as e:
            pass
    return None



ROKU_IP = "192.168.68.57"

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

def create_keypress(key):
    url = f"http://{ROKU_IP}:8060/keypress/{key}"
    requests.post(url)

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

ip = find_roku_ip()
gprint(f"Found IP {ip}")
time.sleep_ms(1000)

gprint("Hint: Tab: Home", clr_idx=4)

while True:
    keys = kb.get_new_keys()
    kb.ext_dir_keys(keys)

    if keys:
        # Directional and special keys
        if "UP" in keys:
            create_keypress("Up")
        elif "DOWN" in keys:
            create_keypress("Down")
        elif "LEFT" in keys:
            create_keypress("Left")
        elif "RIGHT" in keys:
            create_keypress("Right")
        elif "ESC" in keys:
            create_keypress("Back")
        elif "ENT" in keys:
            create_keypress("Select")
        elif "TAB" in keys:
            create_keypress("Home")
        elif "SPC" in keys:
            create_keypress("Lit_%20")
        elif "BSPC" in keys:
            create_keypress("Backspace")
        # elif "OP" in keys and "o":
        #     create_keypress("a")
        else:
            for key in keys:
                create_keypress(f"Lit_{key}")

    time.sleep_ms(10)

