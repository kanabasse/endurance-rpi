import logging
import struct
import time

import serial

from matrix.ht1662c.utils import reverse_byte, split_uint16

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
        self.screen_buffer = {
            self.GREEN: bytearray([0x00] * self.ARRAY_SIZE),
            self.RED: bytearray([0x00] * self.ARRAY_SIZE),
            self.ORANGE: bytearray([0x00] * self.ARRAY_SIZE)
        }
        self.arduino = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        self.logger = logging.getLogger("ht1632c")

    def putraw(self, x, y, data, color, bg):
        cached_data = data if color != self.BLACK else [0xFF] * len(data)

        half_array = self.ARRAY_SIZE // 2
        for i, col in enumerate(cached_data[:half_array]):
            index = x +  i
            if index >= self.ARRAY_SIZE/2:
                break

            shifted_data = reverse_byte(cached_data[i]) << y
            low_bytes, up_bytes = split_uint16(shifted_data)
            if color == self.BLACK:
                for key in self.screen_buffer.keys():
                    self.screen_buffer[key][index + self.ARRAY_SIZE//2] &= ~up_bytes
                    if y < 8: self.screen_buffer[color][index] &= ~low_bytes
            else:
                self.screen_buffer[color][index + self.ARRAY_SIZE//2] = up_bytes
                if y < 8: self.screen_buffer[color][index] = low_bytes

    def putchar(self, x, y, c, font, color, bg):
        """Plot a char c at (x,y) using font"""
        char = font.get(c)
        if c is None:
            self.logger.warning("character '%s' not found in font bitmap", c)
            return
        self.putraw(x, y, char, color, bg)

    def putstr(self, x, y, s, font, color, bg):
        """Plot a string s at (x,y) using font"""
        x_offset = x
        for index, char in enumerate(s):
            char_width = self.charwidth(char, font)
            self.putchar(x_offset, y, char, font, color, bg)
            x_offset += char_width + 1
        return self.strwidth(s, font)

    def charwidth(self, c, font):
        """Return the length of the char c in pixels using font"""
        width = 0
        char_bitmap = font.get(c)
        if char_bitmap is None:
            self.logger.warning("character '%s' not found in font bitmap", c)
            return width
        return len(char_bitmap)

    def strwidth(self, s, font):
        """Return the width of the string s in pixels using font"""
        width = 0
        for index, char in enumerate(s):
            char_width = self.charwidth(char, font)
            width += char_width + (1 if index != (len(s) - 1) else 0)
        return width

    def print(self):
        """Send the screen buffers to the arduino"""
        to_send = struct.pack('64B64B64B',
                              *self.screen_buffer[self.GREEN],
                              *self.screen_buffer[self.RED],
                              *self.screen_buffer[self.ORANGE])
        self.arduino.write(to_send)
        self.logger.debug(f"Sent {len(to_send)} bytes to {self.SERIAL_PORT}")

        # Give some time for the arduino to process
        time.sleep(0.1)

    def debug_screen(self):
        """
        NOT WORKING -- Require to properly merge the RED,GREEN,ORANGE screen buffers
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
