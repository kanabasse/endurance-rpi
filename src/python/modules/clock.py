import datetime
import time

from threading import Thread, Lock
from src.python.modules.moduleinterface import ModuleInterface

from src.python.fonts import font_clock


class TimeReader(Thread):
    REFRESH_DELAY = 1
    lock = Lock()
    current_time = datetime.datetime.fromtimestamp(0)

    def run(self):
        while True:
            self.update_time()
            time.sleep(self.REFRESH_DELAY)

    def update_time(self):
        self.current_time = datetime.datetime.now()

    def get_time(self):
        self.lock.acquire()
        cached_time = self.current_time
        self.lock.release()

        return cached_time

class ClockModule(ModuleInterface):
    SPACING = 1
    time_reader = TimeReader()

    def init(self, screen):
        self.time_reader.start()
        print(f"Initialized module {self.__class__.__name__}...")

    def update(self, screen, pos_x, pos_y):
        now = datetime.datetime.now()
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)

        # Reset position
        x = pos_x
        y = pos_y

        # Draw HH:MM
        x += screen.putstr(x, y, hour, font_clock, screen.GREEN, screen.BLACK) + self.SPACING
        x += screen.putstr(x, y, ':' if now.microsecond > 500000 else ' ', font_clock, screen.ORANGE, screen.BLACK) + self.SPACING
        screen.putstr(x, y, minute, font_clock, screen.GREEN, screen.BLACK)
