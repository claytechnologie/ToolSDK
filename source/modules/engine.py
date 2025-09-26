class Engine:
    
    def __init__(self):
        import modules.loader as loader
        import modules.settings as settings
        from modules.settings import LanguageAsset as languageAsset
        import modules.menu as menu

        # Erst Settings vollständig laden
        self.settings = settings.Settings()
        
        # Dann LanguageAsset mit den vollständigen Settings initialisieren
        self.lang = languageAsset(self.settings)
        
        # Dann den Rest
        self.loader = loader.ModLoader(settings=self.settings)
        self.menu = menu.MenuAsset(self)