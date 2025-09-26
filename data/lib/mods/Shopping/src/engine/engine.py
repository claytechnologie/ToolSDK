import toolos.api as api

class Engine:
    
    def __init__(self, settings_path, sdk, package: dict):
        self.api = api.ToolAPI(settings_path=settings_path, **sdk)
    
    
if __name__ == "__main__":
    
    sdk = {
        "version": "3.0.1",
        "name": "ShoppingToolSDK"
    }

    engine = Engine(sdk=sdk, package={"name": "Shopping", "id": "00-00000", "version": "1.0.0"})
    
    print(engine.Helper.LanguageApi.GetAllTranslationKeys())