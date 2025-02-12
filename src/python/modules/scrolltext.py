from src.python.fonts import font_6x8
from src.python.modules.moduleinterface import ModuleInterface

class ScrollTextModule(ModuleInterface):
    X_OFFSET = 4
    Y_OFFSET = 4
    SPACING = 1

    def __init__(self, text):
        self.str_bytes = 0 # Properly initialized during update()
        self.text = text
        if not self.text.endswith("    "):
            self.text += "    "


    def init(self, screen):
        # self.time_reader.start()
        print(f"Initialized module {self.__class__.__name__}...")
        self.str_bytes = font_6x8.getstr(self.text)


    def update(self, screen, pos_x, pos_y):
        screen.putraw(pos_x, pos_y, self.str_bytes, screen.GREEN, screen.BLACK)
        self.shift()


    def shift(self):
        self.str_bytes = self.str_bytes[1:] + [self.str_bytes[0]]


    def set_text(self, text):
        self.text = text
        self.str_bytes = font_6x8.getstr(self.text)