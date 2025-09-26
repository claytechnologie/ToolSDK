

class Settings:
    
    def __init__(self):
        import json
        self.js = json
        self.SETTINGSPATH = "data/assets/manager/settings.json"
        self.VERSION = None
        self.LANGUAGE = None
        self.AUTHORIZED_IDS = []
        self.HEADER = None
        self.ERRORS = []
        self.INPUTNAME = None
        self.MODPATH = None
        self.MODS_ENABLED = True
        self.SETTINGS = {**self.__dict__}
        
        self.LoadSettings()
        self.ApplySettings()
        
    def CheckIfUpdate(self):
        """Prüft ob Settings aktualisiert wurden"""
        try:
            with open(self.SETTINGSPATH, "r", encoding="utf-8") as f:
                data = self.js.load(f)
                update_flag = data.get("update", False)
                if update_flag:
                    print("🔄 Settings-Update erkannt - lade neu...")
                    # Update-Flag zurücksetzen
                    data["update"] = False
                    with open(self.SETTINGSPATH, "w", encoding="utf-8") as f_write:
                        self.js.dump(data, f_write, indent=4)
                    self.LoadSettings()
                    self.ApplySettings()
                    return True
                return False
        except Exception as e:
            print(f"Fehler beim Prüfen des Update-Flags: {e}")
            return False

    def LoadSettings(self):
        with open (self.SETTINGSPATH, "r", encoding="utf-8") as f:
            self.SETTINGS = self.js.load(f)
            return True
        return False
    
    def ApplySettings(self):
        self.TEMPPATH = self.SETTINGS.get("temppath", "data/assets/temp")
        self.UPDATE = self.SETTINGS.get("update", False)
        self.MODS_ENABLED = self.SETTINGS.get("mods_enabled")
        if self.MODS_ENABLED == "False":
            self.MODS_ENABLED = False
        elif self.MODS_ENABLED == "True":
            self.MODS_ENABLED = True
        self.LANGUAGE = self.SETTINGS.get("language", "de")
        self.VERSION = self.SETTINGS.get("version")
        self.AUTHORIZED_IDS = self.SETTINGS.get("authorized_ids", ["0-000exec"])
        self.HEADER = self.SETTINGS.get("header", "Meine Anwendung")
        self.ERRORS = self.SETTINGS.get("errors", [])
        self.INPUTNAME = self.SETTINGS.get("inputname", "Eingabe")
        self.MODPATH = self.SETTINGS.get("modpath", "data/lib/mods")
        self.SETTINGSPATH = self.SETTINGS.get("settingspath", "data/assets/manager/settings.json")
        self.LANGUAGEPATH = self.SETTINGS.get("languagepath", "data/assets/manager/lang")
        return True
    
class LanguageAsset:
    
    def __init__(self, settings):
        self.settings = settings
        self.lang = self.LoadLanguageData(self.settings.LANGUAGE)
        self.HEADER = self.lang.get("header")
        self.SETTINGS = self.lang.get("settings")
        self.DIARY = self.lang.get("book")
        self.EXIT = self.lang.get("exit")
        self.PACKAGE_MANAGEMENT = self.lang.get("package_management")
        self.APP_RUNNING = self.lang.get("app_is_running")
        self.APP_NOT_RUNNING = self.lang.get("app_is_not_running")
        self.SETTINGS_CHANGED = self.lang.get("setting_changed")
        self.INPUT_PROMPT = self.lang.get("input")
        self.ASK_EXIT = self.lang.get("ask_exit")
        self.INVALID_OPTION = self.lang.get("invalid_option")
        self.SETTINGS_SAVED = self.lang.get("setting_saved")
        self.MENU_RELOADED = self.lang.get("menu_reloaded")
        self.WARNING = self.lang.get("warning")
        self.EXIT_SELECTED = self.lang.get("exit_selected")
        self.EXITING_APP = self.lang.get("exiting_app")
        
    def LoadLanguageData(self, lang="de"):
        import json
        try:
            with open(f"{self.settings.LANGUAGEPATH}/{lang}.json", 'r', encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(f"{self.settings.LANGUAGEPATH}/de.json", 'r', encoding="utf-8") as f:
                return json.load(f)
            
    def Translate(self, key):
        return self.lang.get(key, key)
    
    def GetAllTranslationKeys(self):
        return list(self.lang.keys())
    
    def GetAvailableLanguages(self):
        import os
        files = os.listdir(self.settings.LANGUAGEPATH)
        languages = [f.split('.')[0] for f in files if f.endswith('.json')]
        return languages
    
    def Reload(self):
        self.lang = self.LoadLanguageData(self.settings.LANGUAGE)
        
        