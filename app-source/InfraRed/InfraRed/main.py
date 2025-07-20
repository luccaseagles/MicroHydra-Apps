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

import esp32

def hex_to_bin(hex_value, bits=32):
    """Convert a hex value to a binary string with a fixed number of bits."""
    bin_value = bin(int(hex_value, 16))[2:]  # Convert to binary and strip the '0b'
    return pad_binary_string(bin_value, bits)

def pad_binary_string(bin_value, bits):
    """Pad a binary string with leading zeros to ensure it has the specified number of bits."""
    if len(bin_value) < bits:
        return '0' * (bits - len(bin_value)) + bin_value
    return bin_value

def generate_raw_timing(binary_string):
    """Convert binary string to raw timing list based on NEC protocol."""
    timing = []
    for bit in binary_string:
        if bit == '1':
            timing.extend([560, 1690])
        else:
            timing.extend([560, 560])
    return timing

def nec_ir_signal(address, command):
    """Convert NEC IR signal address and command to raw timing format."""
    # Convert address and command to binary strings
    address = address.replace(" ", "")
    command = command.replace(" ", "")
    address_bin = hex_to_bin(address)
    address_inv_bin = hex_to_bin(hex(int(address, 16) ^ 0xFFFFFFFF))[2:]
    address_inv_bin = pad_binary_string(address_inv_bin, 32)
    command_bin = hex_to_bin(command)
    command_inv_bin = hex_to_bin(hex(int(command, 16) ^ 0xFFFFFFFF))[2:]
    command_inv_bin = pad_binary_string(command_inv_bin, 32)

    # Start of transmission (header)
    raw_signal = [9000, 4500]

    # Append address and inverted address timings
    raw_signal += generate_raw_timing(address_bin)
    raw_signal += generate_raw_timing(address_inv_bin)

    # Append command and inverted command timings
    raw_signal += generate_raw_timing(command_bin)
    raw_signal += generate_raw_timing(command_inv_bin)

    # Stop bit
    raw_signal.append(560)

    return raw_signal

def format_raw_timing(raw_signal):
    """Format raw timing list into a string for display."""
    return ' '.join(map(str, raw_signal))

def convert(address, command):
    return nec_ir_signal(address, command)

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

tx = UpyIrTx(0, 44)
gprint("Inited")
time.sleep_ms(1000)
raw_signal = nec_ir_signal("20", "23")
tx.send_raw(raw_signal)
gprint("Power ON signal sent.")

