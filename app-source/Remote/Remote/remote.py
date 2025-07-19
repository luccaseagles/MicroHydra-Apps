"""
MicroHydra Roku Remote Control

Version: 1.0

Control a Roku device over Wi-Fi using MicroPython.
Displays the pressed keys and sends them as Roku remote commands.
"""

import time

try:
    import urequests
except ImportError:
    print("urequests module required!")

# Stub Display class (replace with your actual display driver)
class Display:
    def fill(self, color):
        pass  # Implement actual fill

    def text(self, text, x, y, color):
        print(f"[DISPLAY] {text} at ({x},{y})")

    def show(self):
        pass  # Implement actual screen update

# Stub UserInput class (replace with actual input handling)
class UserInput:
    def get_new_keys(self):
        # Return a list like ["UP"] or ["A"]
        return []  # Simulate keypresses here for testing

# Roku remote class using HTTP (ECP API)
class RokuRemote:
    def __init__(self, ip):
        self.base_url = f"http://{ip}:8060"

    def keypress(self, key):
        url = f"{self.base_url}/keypress/{key}"
        try:
            response = urequests.post(url)
            response.close()
            print(f"Sent: {key}")
        except Exception as e:
            print("Error sending key:", key, e)

# Dummy config palette
class Config:
    def __init__(self):
        self.palette = [
            0x000000,  # 0 - Black
            0xFFFFFF,  # 1 - White
            0x202020,  # 2 - Background (Dark Gray)
            0xFF0000,  # 3 - Red
            0x00FF00,  # 4 - Green
            0x0000FF,  # 5 - Blue
            0xFFFF00,  # 6 - Yellow
            0x00FFFF,  # 7 - Cyan
            0xFF00FF,  # 8 - Magenta (Text)
        ]

# Constants
_DISPLAY_WIDTH = const(240)
_DISPLAY_HEIGHT = const(135)
_DISPLAY_WIDTH_HALF = const(_DISPLAY_WIDTH // 2)
_CHAR_WIDTH = const(8)
_CHAR_WIDTH_HALF = const(_CHAR_WIDTH // 2)

# Init objects
DISPLAY = Display()
INPUT = UserInput()
CONFIG = Config()

# Set your Roku's IP address here
ROKU_IP = "192.168.1.100"
roku = RokuRemote(ROKU_IP)

def main_loop():
    current_text = "Ready"

    while True:
        keys = INPUT.get_new_keys()
        if keys:
            key_str = str(keys)
            current_text = key_str

            # Map keypress to Roku commands
            if "UP" in keys:
                roku.keypress("Up")
            elif "DOWN" in keys:
                roku.keypress("Down")
            elif "LEFT" in keys:
                roku.keypress("Left")
            elif "RIGHT" in keys:
                roku.keypress("Right")
            elif "A" in keys:
                roku.keypress("Home")
            elif "B" in keys:
                roku.keypress("Back")
            elif "ENTER" in keys:
                roku.keypress("Select")

        # Display logic
        DISPLAY.fill(CONFIG.palette[2])
        DISPLAY.text(
            text=current_text,
            x=_DISPLAY_WIDTH_HALF - (len(current_text) * _CHAR_WIDTH_HALF),
            y=50,
            color=CONFIG.palette[8],
        )
        DISPLAY.show()
        time.sleep_ms(10)

main_loop()
