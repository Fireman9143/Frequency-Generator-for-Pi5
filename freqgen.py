import gpiod
import time

# Configuration
CHIP = "/dev/gpiochip0"  # Default GPIO chip
LINE = 18  # GPIO pin to use
TARGET_FREQ = 14000000  # 14 MHz target frequency

# Calculate delay for toggling
toggle_delay = 1 / (2 * TARGET_FREQ)  # Half period for square wave

# Initialize GPIO line
chip = gpiod.Chip(CHIP)
line = chip.get_line(LINE)

# Configure the GPIO line for output
config = gpiod.LineRequest()
config.consumer = "SignalGenerator"
config.request_type = gpiod.LINE_REQ_DIR_OUT
line.request(config)

try:
    print(f"Generating ~{TARGET_FREQ / 1e6} MHz signal on GPIO{LINE}. Press Ctrl+C to stop.")
    while True:
        line.set_value(1)
        time.sleep(toggle_delay)
        line.set_value(0)
        time.sleep(toggle_delay)

except KeyboardInterrupt:
    print("Stopping signal generation...")

finally:
    line.release()
    print("Program terminated.")
