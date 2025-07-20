"""A simple app to query Wikipedia for page summaries."""
# import requests, network, time
import time
# from machine import Pin, freq
from lib.display import Display
# from lib.userinput import UserInput
from lib.hydra.config import Config
from lib.device import Device
from lib.hydra.popup import UIOverlay
from font import vga1_8x16 as font

from machine import Pin, disable_irq, enable_irq
from micropython import const

from NEC2RAW import *

import esp32


tft = Display(use_tiny_buf=("spi_ram" not in Device))

config = Config()

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



# IR TX class for ESP32
# micropython v1.17 - v1.18(latest as of 2022/5)

class UpyIrTx():

    def __init__(self, ch, pin, freq=38000, duty=99, idle_level=0):
        self._raise = False
        if freq <= 0 or duty <= 0 or duty >= 100 or ch < 0 or ch > 7:
            raise(IndexError())
        if idle_level:
            self._rmt = esp32.RMT(ch, pin=pin, clock_div=80, tx_carrier=(freq, (100-duty), 0), idle_level=True)
            self._posi = 0
        else:
            self._rmt = esp32.RMT(ch, pin=pin, clock_div=80, tx_carrier=(freq, duty, 1), idle_level=False)
            self._posi = 1

    def send_raw(self, signal_tuple):
        # Blocking until transmission
        # Value[us] must be less than 32,768(15bit)
        if signal_tuple:
            self._rmt.write_pulses(signal_tuple, self._posi)
            self._rmt.wait_done(timeout=2000)
        return(True)
    
    def send(self, signal_tuple):
        # Blocking until transmission
        # Value[us] is free
        if not signal_tuple:
            return(True)
        overindex = []
        offsets = []
        cumsum = 0
        len_signal = len(signal_tuple)
        if len_signal % 2 == 0:
            return(False)
        for i in range(len_signal):
            if signal_tuple[i] >= 32768:
                if i % 2 == 0:
                    return(False)
                else:
                    overindex.append(i)
                    offsets.append(cumsum)
                    cumsum = 0
            else:
                cumsum += signal_tuple[i]
        if len(overindex) == 0:
            self._rmt.write_pulses(signal_tuple, self._posi)
            self._rmt.wait_done(timeout=2000)
        else:
            last_index = 0
            for i in range(len(overindex)):
                self._rmt.write_pulses(signal_tuple[last_index: overindex[i]], self._posi)
                time.sleep_us(signal_tuple[overindex[i]]+offsets[i])
                last_index = overindex[i] + 1
            self._rmt.write_pulses(signal_tuple[last_index: len_signal], self._posi)
            self._rmt.wait_done(timeout=2000)
        return(True)

    def send_cls(self, ir_rx):
        # Blocking until transmission
        if ir_rx.get_record_size() != 0:
            return(self.send(ir_rx.get_calibrate_list()))
        else:
            return(False)


# Example: NEC protocol, Samsung TV power toggle (address 0xE0E0, command 0x40BF)
# You'll need to find the right code for YOUR TV
# NEC_ADDRESS = 0xE0E0
# NEC_COMMAND = 0x40BF

# Or you can use raw pulses directly if you have them, e.g.:
# RAW_SIGNAL = [4500, 4500, 560, 1690, ...] # Your recorded signal here

# Assume convert(address, command) returns the right raw waveform
# from NEC2RAW import convert
# raw_signal = convert(NEC_ADDRESS, NEC_COMMAND)

# Setup transmitter (Pin 44, Channel 0)
tx = UpyIrTx(0, 44)

# # Send signal
# tx.send_raw(raw_signal)
gprint("Inited")
time.sleep_ms(1000)


# Your NEC code
POWER_ON_HEX = "20DF23DC"

# Build the NEC pulse sequence
binary_string = hex_to_bin(POWER_ON_HEX, 32)
raw_signal = [9000, 4500]
raw_signal += generate_raw_timing(binary_string)
raw_signal.append(560)

# Transmit
tx.send_raw(raw_signal)
gprint("Power ON signal sent.")

