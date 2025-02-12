from fonts import font_clock


from modules.clock import ClockModule
from modules.manager import ModuleManager
from modules.scrolltext import ScrollTextModule
from src.python.ht1662c.ht1632c import HT1632C


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
    ht1632c.putstr(0, 0,"1234", font_clock, 0, 0)
    ht1632c.print()


module_manager = ModuleManager()
module_manager.register(ClockModule(), 4, 1)
scroll_text_module = ScrollTextModule('Test screen')
module_manager.register(scroll_text_module, 0, 9)
# module_manager.register(TemperatureModule(), 4, 9)

ht1632c = HT1632C()
module_manager.init_modules(ht1632c)
while True:
    module_manager.update(ht1632c)
    ht1632c.print()

    # test1()
    # test2()
