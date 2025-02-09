import logging
import time

from fonts import font_clock

import serial

from modules.clock import ClockModule
from modules.manager import ModuleManager
from modules.scrolltext import ScrollTextModule

LOG = logging.getLogger(__name__)

class HT1632C2:
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
        self.arduino.write(self.screen_buffer)
        print(f"Sent {len(self.screen_buffer)} bytes to {self.SERIAL_PORT}")

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

def reverse_byte(byte):
    byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)  # Swap nibbles
    byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)  # Swap 2-bit pairs
    byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)  # Swap individual bits
    return byte

def split_uint16(value):
    """
    Splits a 16-bit unsigned integer into two 8-bit unsigned integers.

    :param value: uint16 (0 to 65535)
    :return: (low_byte, high_byte) as two uint8 values
    """
    low_byte = value & 0xFF        # Extract lower 8 bits (Least Significant Byte)
    high_byte = (value >> 8) & 0xFF  # Extract upper 8 bits (Most Significant Byte)
    return low_byte, high_byte

def test1():
    new_array = bytearray([0xFF] * 16) + bytearray([0x00] * 16) + bytearray(
        [0x00] * 16) + bytearray([0x00] * 16)
    ht1632c.add_to_screen(new_array)
    ht1632c.print()

    new_array = bytearray([0x00] * 16) + bytearray([0xFF] * 16) + bytearray(
        [0x00] * 16) + bytearray([0x00] * 16)
    ht1632c.add_to_screen(new_array)
    ht1632c.print()

    new_array = bytearray([0x00] * 16) + bytearray([0x00] * 16) + bytearray(
        [0xFF] * 16) + bytearray([0x00] * 16)
    ht1632c.add_to_screen(new_array)
    ht1632c.print()

    new_array = bytearray([0x00] * 16) + bytearray([0x00] * 16) + bytearray(
        [0x00] * 16) + bytearray([0xFF] * 16)
    ht1632c.add_to_screen(new_array)
    ht1632c.print()

    new_array = bytearray([0x00] * 64)
    ht1632c.set_to_screen(new_array)
    ht1632c.print()


def test2():
    ht1632c.putstr(0,0,"1234", font_clock, 0, 0)
    ht1632c.print()


module_manager = ModuleManager()
module_manager.register(ClockModule(), 4, 1)
scroll_text_module = ScrollTextModule('Test screen')
module_manager.register(scroll_text_module, 0, 9)
# module_manager.register(TemperatureModule(), 4, 9)

ht1632c = HT1632C2()
module_manager.init_modules(ht1632c)
while True:
    module_manager.update(ht1632c)
    ht1632c.print()

    # test1()
    # test2()
