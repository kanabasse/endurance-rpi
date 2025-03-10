import logging
from matrix.modules.clock import ClockModule
from matrix.modules.module_data import ModuleData
from matrix.modules.scrolltext import ScrollTextModule
from matrix.ht1662c.ht1632c import HT1632C
# from matrix.modules.temperature import TemperatureModule


class Matrix:
  def __init__(self):
    self.module_priorities = {}

    self.logger = logging.getLogger("matrix")
    self.ht1632c = HT1632C()

    # TODO: run from somewhere else
    clock_module = ClockModule()
    self.register(clock_module, 4, 0, 0)

    scroll_text_module = ScrollTextModule('Test screen')
    self.register(scroll_text_module, 0, 8, 0)


  def register(self, new_module, pos_x, pos_y, priority):
    """
    Adds a module to the dictionary with the specified priority.
    :param new_module: Module to add
    :param pos_x:      x position
    :param pos_y:      y position
    :param priority:   display priority, lower value means lower priority
    :return:
    """
    if not priority in self.module_priorities:
      self.module_priorities[priority] = []
    self.module_priorities[priority].append(ModuleData(new_module, pos_x, pos_y))

    self.logger.debug(f"Initializing module {new_module.__class__.__name__}...")
    new_module.init_screen(self.ht1632c)

  def add_module(self, module, pos_x, pos_y, priority):
    self.register(module, pos_x, pos_y, priority)

  def update_module(self, screen):
    """Update modules according to module priority."""
    if len(self.module_priorities) == 0:
      return
    for i in range(max(self.module_priorities.keys()) + 1):
      if i in self.module_priorities.keys():
        for module_data in self.module_priorities[i]:
          module_data.module.update_screen(screen, module_data.pos_x, module_data.pos_y)

  def get_modules_by_class(self, module_class):
    modules = []
    for priority in self.module_priorities.keys():
      for module_data in self.module_priorities[priority]:
        if module_class == module_data.module.__class__.__name__:
          modules.append(module_data.module)
    return modules

  def get_module(self, id):
    for priority in self.module_priorities.keys():
      for module_data in self.module_priorities[priority]:
        if id == str(module_data.module.id):
          return module_data.module
    return None

  def remove_module(self, id):
    for priority in self.module_priorities.keys():
      for module_data in self.module_priorities[priority]:
        if id == str(module_data.module.id):
          self.module_priorities[priority].remove(module_data)
          return True
    return False

  def run_update_loop(self):
    while True:
      self.update_module(self.ht1632c)
      self.ht1632c.print()