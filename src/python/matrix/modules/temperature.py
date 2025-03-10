import glob
import time
from threading import Thread, Lock

from matrix.modules.module_interface import ModuleInterface


class TemperatureReader(Thread):
    REFRESH_DELAY = 1
    lock = Lock()
    current_temperature = 0

    # Temperature is exposed as a block device on fs
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    def run(self):
        while True:
            self.update_temperature()
            time.sleep(self.REFRESH_DELAY)

    def update_temperature(self):
        cached_temperature = self.read_temperature()

        self.lock.acquire()
        self.current_temperature = cached_temperature
        self.lock.release()

    def read_temperature(self):
        lines = self.__read_temperature_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__read_temperature_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def __read_temperature_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_temperature(self):
        self.lock.acquire()
        cached_temperature = self.current_temperature
        self.lock.release()

        return cached_temperature


class TemperatureModule(ModuleInterface):
    SPACING = 1
    temperature_reader = TemperatureReader()

    def init_screen(self, screen):
        self.temperature_reader.start()
        print(f"Initialized module {self.__class__.__name__}...")

    def update_screen(self, screen, pos_x, pos_y):
        screen.putstr(pos_x, pos_y, str(round(self.temperature_reader.get_temperature(), 1)) + 'c',
                      screen.font5x8, screen.GREEN, screen.BLACK)