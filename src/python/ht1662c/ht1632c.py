import logging
import struct
import time

import serial

from src.python.ht1662c.utils import reverse_byte, split_uint16, rainbow

LOG = logging.getLogger(__name__)


class HT1632C:
    BLACK = 0
    GREEN = 1
    RED = 2
    ORANGE = 3
    TRANSPARENT = 0xff

    SERIAL_PORT = "/dev/ttyACM0"  # Adjust this if needed
    BAUD_RATE = 921600  # Adjust to match your device's settings
    ARRAY_SIZE = 64

    def __init__(self):
        self.screen_buffer = bytearray([0x00] * self.ARRAY_SIZE)
        self.arduino = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        pass

    def putraw(self, x, y, data, color, bg):
        half_array = self.ARRAY_SIZE // 2
        for i, col in enumerate(data[:half_array]):
            index = x +  i
            if index > self.ARRAY_SIZE/2:
                break

            shifted_data = reverse_byte(data[i]) << y
            low_bytes, up_bytes = split_uint16(shifted_data)
            if index < self.ARRAY_SIZE and y < 8:
                self.screen_buffer[x + i] = low_bytes
            if index < self.ARRAY_SIZE/2:
                self.screen_buffer[self.ARRAY_SIZE//2 + x + i] = up_bytes

        # self.debug_screen()

    def putchar(self, x, y, c, font, color, bg):
        char = font.get(c)
        if c is None:
            LOG.warning("character '%s' not found in font bitmap", c)
            return
        self.putraw(x, y, char, color, bg)

    def putstr(self, x, y, s, font, color, bg):
        x_offset = x
        for index, char in enumerate(s):
            char_width = self.charwidth(char, font)
            self.putchar(x_offset, y, char, font, color, bg)
            x_offset += char_width + 1
        return self.strwidth(s, font)

    def charwidth(self, c, font):
        width = 0
        char_bitmap = font.get(c)
        if char_bitmap is None:
            LOG.warning("character '%s' not found in font bitmap", c)
            return width
        return len(char_bitmap)

    def strwidth(self, s, font):
        width = 0
        for index, char in enumerate(s):
            char_width = self.charwidth(char, font)
            width += char_width + (1 if index != (len(s) - 1) else 0)
        return width

    def add_to_screen(self, data):
        for i, byte in enumerate(data):
            self.screen_buffer[i] = self.screen_buffer[i] or byte

    def set_to_screen(self, data):
        self.screen_buffer = data

    def print(self):
        # color = random.randint(1,3)
        to_send = struct.pack('B64B?', next(rainbow), *self.screen_buffer, True)

        self.arduino.write(to_send)
        print(f"Sent {len(to_send)} bytes to {self.SERIAL_PORT}")

        # Give some time to process
        time.sleep(0.1)

    def debug_screen(self):
        """
        Plots a 32x16 binary image onto the screen buffer.

        :param screen: bytearray representing the 32x16 screen (512 bytes).
        :param data: List of 32 uint16 values, each bit representing a pixel (1=on, 0=off).
        """
        SCREEN_WIDTH = 64
        SCREEN_HEIGHT = 8
        screen = bytearray(32 * 16)

        # Ensure data has exactly 32 uint16 values
        if len(self.screen_buffer) != SCREEN_WIDTH:
            raise ValueError("Data must contain exactly 32 uint16 values.")

        for x in range(SCREEN_WIDTH):
            column = self.screen_buffer[x]  # Get uint16 value representing this column
            for y in range(SCREEN_HEIGHT):
                pixel_state = (column >> y) & 1  # Extract bit y from uint16
                index = y * SCREEN_WIDTH + x  # Compute linear index in screen buffer
                screen[index] = pixel_state  # Store 1 or 0

        for row in range(8):
            print("".join("█" if screen[row * 2 * 32 + col ] else "." for col in range(32)))

        for row in range(8):
            print("".join("█" if screen[(row * 2 + 1) * 32 + col] else "." for col in range(32)))
