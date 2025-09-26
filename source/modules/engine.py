import toolos.api as api
class Engine(api.Api):
    
    def __init__(self, settings_path):
        super().__init__(settings_path=settings_path)
        import source.modules.menu as menu
        import source.modules.loader as loader
        self.menu = menu.MenuAsset(self)
        self.loader = loader.ModLoader(self.Settings)