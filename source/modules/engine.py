import toolos as engine
class Engine(engine.Api):
    
    def __init__(self, settings_path=None, standard_library=True):
        super().__init__(settings_path=settings_path, standard_language_library=standard_library)
        import modules.menu as menu
        import modules.loader as loader
        self.menu = menu.MenuAsset(self)
        self.loader = loader.ModLoader(self.Settings)