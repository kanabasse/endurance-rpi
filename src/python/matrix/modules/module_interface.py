from uuid import uuid4


class ModuleInterface:
    def __init__(self):
        self.id = uuid4()

    def init_screen(self, screen):
        pass

    def update_screen(self, screen, pos_x, pos_y):
        pass