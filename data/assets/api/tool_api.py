    #? ################  SETTINGS API #####################

class SettingsAPI:
    
    def __init__(self):
        self.SETTINGSPATH = "data/assets/manager/settings.json"
        self.SETTINGS = self.LoadSettings()
        self.VERSION = self.SETTINGS.get("version")
        self.LANGUAGE = self.SETTINGS.get("language")
        self.PACKAGEPATH = self.SETTINGS.get("packagepath")
        self.CACHEPATH = self.SETTINGS.get("cachepath")
        self.TEMPPATH = self.SETTINGS.get("temppath")
        self.LOGPATH = self.SETTINGS.get("logpath")
        self.APIPATH = self.SETTINGS.get("apipath")
        self.LANGUAGEPATH = self.SETTINGS.get("languagepath")
        
    def LoadSettings(self):
        import json
        with open(self.SETTINGSPATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    #? ################  CACHE API #####################

class CacheAPI:
    
    def __init__(self, cache_path):
        self.CACHEPATH = cache_path
        
    def WriteCacheFile(self, filename, content):
        with open(f"{self.CACHEPATH}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
            
    def ReadCacheFile(self, filename):
        with open(f"{self.CACHEPATH}/{filename}", 'r', encoding='utf-8') as f:
            return f.read()
    
    def AddContent(self, filename, content):
        with open(f"{self.CACHEPATH}/{filename}", 'a', encoding='utf-8') as f:
            f.write(content + "\n")
            
    def RemoveCacheFile(self, filename):
        import os
        os.remove(f"{self.CACHEPATH}/{filename}")

    #? ################  TEMP API #####################

class TempAPI:
    
    def __init__(self, temp_path):
        self.TEMPPATH = temp_path
        
    def WriteTempFile(self, filename, content):
        with open(f"{self.TEMPPATH}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
            
    def ReadTempFile(self, filename):
        with open(f"{self.TEMPPATH}/{filename}", 'r', encoding='utf-8') as f:
            return f.read()
        
    def AddContent(self, filename, content):
        with open(f"{self.TEMPPATH}/{filename}", 'a', encoding='utf-8') as f:
            f.write(content + "\n")
    
    def TempExists(self, filename):
        import os
        return os.path.exists(f"{self.TEMPPATH}/{filename}")
    
    def RemoveTempFile(self, filename):
        import os
        os.remove(f"{self.TEMPPATH}/{filename}")

    #? ################  PACKAGE API #####################

class PackageAPI:
    
    def __init__(self, package_path):
        self.PACKAGEPATH = package_path
        self.isLoggedIn = False
        self.USERNAME = None
        
    def Login(self, username, password):
        if username == "admin" and password == "password":
            self.isLoggedIn = True
            self.USERNAME = username
            return True
        return False
    
    def Logout(self):
        self.isLoggedIn = False
        self.USERNAME = None
        
    def WritePackageFile(self, filename, content):
        with open(f"{self.PACKAGEPATH}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
            
    def ReadPackageFile(self, filename):
        with open(f"{self.PACKAGEPATH}/{filename}", 'r', encoding='utf-8') as f:
            return f.read()
        
    def AddContent(self, filename, content):
        with open(f"{self.PACKAGEPATH}/{filename}", 'a', encoding='utf-8') as f:
            f.write(content + "\n")
    
    def RemovePackageFile(self, filename):
        import os
        os.remove(f"{self.PACKAGEPATH}/{filename}")
        
    #? ################  LOG API #####################
        
class LogAPI:
    
    def __init__(self, log_path):
        self.LOGPATH = log_path
        
    def WriteLog(self, filename, message):
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        with open(f"{self.LOGPATH}/{filename}", 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
            
    def ReadLog(self, filename):
        with open(f"{self.LOGPATH}/{filename}", 'r', encoding='utf-8') as f:
            return f.read()
        
    def DeleteLog(self, filename):
        import os
        os.remove(f"{self.LOGPATH}/{filename}")
        
    def ClearLog(self, filename):
        with open(f"{self.LOGPATH}/{filename}", 'w') as f:
            f.write("")

    #? ################  MANAGER API #####################

class ManagerAPI:
    
    def __init__(self, api_path):
        self.API_PATH = api_path
        
        
        
    #? ################  HELPER API #####################

class HelperAPI:
    
    def __init__(self, settings):
        self.Settings = settings

    def GetVersion(self):
        return self.Settings.VERSION

    def GetLanguage(self):
        return self.Settings.LANGUAGE
    
    #? ################  LANGUAGE API #####################

class LanguageAPI:
    
    def __init__(self, settings):
        self.Settings = settings
        self.LANGUAGE = settings.LANGUAGE
        self.LANGUAGEPATH = settings.LANGUAGEPATH
        self.PACKAGES = []
        self.language_data = self.load_language_data(self.LANGUAGE)
        
    #? Core Functions

    # Reloading language data (e.g. after changing language in settings or adding new language-packs)
    def Reload(self):
        """Reloading Language-Data and applied Language-Packages"""
        self.LANGUAGE = self.Settings.LANGUAGE
        self.language_data = self.load_language_data(self.LANGUAGE)
        if self.PACKAGES:
            for package in self.PACKAGES:
                if package["language"] == self.LANGUAGE:
                    self.language_data.update(package["data"])
    
    # Loading Original Language-Data json formats from /assets/manager/lang/{'de', 'en', 'ru',..}.json    
    def load_language_data(self, language):
        """Loading Language-Data by parameter: language"""
        import json
        try:
            with open(f"{self.LANGUAGEPATH}/{language}.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(f"{self.LANGUAGEPATH}/de.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        
    #? Interaction Functions
    
    def Translate(self, key):
        """Translating Keyword by key with current language-data"""
        return self.language_data.get(key, key)
    
    def GetAllTranslationKeys(self):
        """Returning all translation keys"""
        return list(self.language_data.keys())
    
    def GetAvailableLanguages(self):
        """Returning all available languages from {self.LANGUAGEPATH}"""
        import os
        files = os.listdir(self.LANGUAGEPATH)
        languages = [f.split('.')[0] for f in files if f.endswith('.json')]
        return languages
    
    def AddLanguagePackage(self, language, datapath):
        import json
        with open(datapath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.PACKAGES.append({"language": language, "data": data})

    #? ################  TOOL API #####################

class ToolAPI:
    
    def __init__(self, **sdk):
        """Requires sdk{version, name}"""
        self.SDK = sdk
        self.SDK_VERSION = sdk.get("version")
        self.SDK_NAME = sdk.get("name")
        self.Settings = SettingsAPI()
        if self.CheckCompatibility(self.Settings.VERSION, self.SDK_VERSION):
            self.Cache = CacheAPI(self.Settings.CACHEPATH)
            self.Temp = TempAPI(self.Settings.TEMPPATH)
            self.Package = PackageAPI(self.Settings.PACKAGEPATH)
            self.Log = LogAPI(self.Settings.LOGPATH)
            self.manager = ManagerAPI(self.Settings.APIPATH)
            self.helper = HelperAPI(self.Settings)
            self.language = LanguageAPI(self.Settings)
        
    
    def CheckCompatibility(self, api_version, sdk_version: str):
        major, minor, patch = sdk_version.split(".")
        if major != api_version.split(".")[0]:
            raise ValueError(f"Inkompatible Versionen: API {api_version} != SDK {sdk_version}")
        return True
    



    #? ################  Testing #####################

if __name__ == "__main__":
    sdk = {"version": "3.0.1", "name": "ShoppingToolSDK"}
    api = ToolAPI(**sdk)
    
    #?  Test aller Sprachen 
    def test_languages():
        languages = api.language.GetAvailableLanguages()
        print(f"🌍 Verfügbare Sprachen: {languages}\n")
        for lang in languages:
            api.Settings.LANGUAGE = lang
            api.language.Reload()
            for key in api.language.GetAllTranslationKeys():
                print(f"{key}: {api.language.Translate(key)}")
                
    test_languages()