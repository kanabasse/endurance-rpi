from fonts import font_6x8
from matrix.modules.module_interface import ModuleInterface


class ScrollTextModule(ModuleInterface):
  MIN_SPACING = "   "
  X_OFFSET = 4
  Y_OFFSET = 4
  SPACING = 1

  def __init__(self, text):
    super().__init__()
    self.str_bytes = [] # Properly initialized during update_screen()
    self.set_text(text)

  def update_screen(self, screen, pos_x, pos_y):
    screen.putraw(pos_x, pos_y, self.str_bytes, screen.GREEN, screen.BLACK)
    self.__shift()

  def __shift(self):
    self.str_bytes = self.str_bytes[1:] + [self.str_bytes[0]]

  def set_text(self, text):
    cached_text = text
    if not cached_text.endswith(self.MIN_SPACING):
      cached_text += self.MIN_SPACING
    self.str_bytes = font_6x8.getstr(cached_text)
