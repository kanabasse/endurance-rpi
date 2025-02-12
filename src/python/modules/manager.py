class ModuleData:
    def __init__(self, module, pos_x, pos_y):
        self.module = module
        self.pos_x = pos_x
        self.pos_y = pos_y

class ModuleManager:
    module_datas = []

    def register(self, new_module, pos_x, pos_y):
        self.module_datas.append(ModuleData(new_module, pos_x, pos_y))

    def init_modules(self, screen):
        for module_data in self.module_datas:
            module_data.module.init(screen)

    def update(self, screen):
        for module_data in self.module_datas:
            module_data.module.update(screen, module_data.pos_x, module_data.pos_y)