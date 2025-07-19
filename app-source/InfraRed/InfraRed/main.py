from UpyIrTx import UpyIrTx
import time

# Example: NEC protocol, Samsung TV power toggle (address 0xE0E0, command 0x40BF)
# You'll need to find the right code for YOUR TV
NEC_ADDRESS = 0xE0E0
NEC_COMMAND = 0x40BF

# Or you can use raw pulses directly if you have them, e.g.:
# RAW_SIGNAL = [4500, 4500, 560, 1690, ...] # Your recorded signal here

# Assume convert(address, command) returns the right raw waveform
from NEC2RAW import convert
raw_signal = convert(NEC_ADDRESS, NEC_COMMAND)

# Setup transmitter (Pin 44, Channel 0)
tx = UpyIrTx(0, 44)

# Send signal
tx.send_raw(raw_signal)
print("Power signal sent.")
