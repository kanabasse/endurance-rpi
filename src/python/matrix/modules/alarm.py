import datetime

from fonts import font_6x8
from matrix.modules.scrolltext import ScrollTextModule

class AlarmModule(ScrollTextModule):
  SPACING = 1

  def __init__(self, text, date):
    super().__init__(text)
    self.date = date
    self.text = text
    self.enabled = False

  def set_text(self, text):
    self.text = text
    super().set_text(text)

  def update_screen(self, screen, pos_x, pos_y):
    if not self.enabled:
      return

    now = datetime.datetime.now()
    if self.date < now:
      if now.microsecond > 500000:
        screen.putchar(pos_x, pos_y, 'clock', font_6x8, screen.GREEN, screen.BLACK)
      else:
        screen.putchar(pos_x, pos_y, 'clock', font_6x8, screen.BLACK, screen.BLACK)
      screen.putraw(pos_x + screen.charwidth('clock', font_6x8), pos_y, [0x00], screen.BLACK, screen.BLACK)
      super().update_screen(screen, pos_x + screen.charwidth('clock', font_6x8) + 1, pos_y)