import os

class MenuAsset:
    
    def __init__(self, api):
        self.api = api
        self.HEADER: str = None
        self.MENU: list = None
        self.EXIT = False
        self.dMENU = []
        self.ERRORS = None
        self.RELOAD = False
        self.TEMPPATH = None
    
    
    def ClearConsole(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def ReloadMenu(self, settings):
        """Lädt Menu mit neuen Settings neu"""
        if self.RELOAD:
            self.RELOAD = False
            self.SetSettings(settings)
            self.api.lang.Reload()

            self.ClearConsole()
            print(self.api.lang.MENU_RELOADED)
            # Kurz warten damit User die Änderung sieht
            import time
            time.sleep(1)
        
        
        
    def ShowHeader(self, header=None):
        if header:
            print("----------------------")
            print(header)
            print("----------------------")
            print()
        else:
            print("----------------------")
            print(self.api.lang.HEADER)
            print("----------------------")
            print()
            
    def ReadMenuData(self):
        for item in self.MENU:
                self.dMENU.append(item.get("build", {}).get('mesh'))
            
    def ShowMenu(self, menu: list = None, action=None):
        if self.dMENU and menu is None:
            for i, name in enumerate(self.dMENU):


                print(i, name)
        else:
            for i, name in enumerate(menu):
                print(i, name)
        if action == 0:
            self.dMENU = menu
                
            
            
    def ShowText(self ,text: str):
        print(text)
        
    
    def LoadModMenus(self, mods):
        modmenus = mods.MODDED
        for mod in modmenus:
            self.MENU.append(mod)
            
            
    def ShowPossibleErrors(self):
        if self.ERRORS:
            for error in self.ERRORS:
                print(self.api.lang.WARNING, error)
            
    def DoMenuSelection(self, selection: int):
        if selection < len(self.MENU):
            self.startMenu(selection)
        else:
            return None
        
    def SetSettings(self, settings):
        
        self.HEADER = settings.HEADER
        self.ERRORS = settings.ERRORS
        self.mods_enabled = settings.MODS_ENABLED
        self.INPUTNAME = settings.INPUTNAME
        self.VERSION = settings.VERSION
        self.LANGUAGE = settings.LANGUAGE
        self.TEMPPATH = settings.TEMPPATH
        
        
    def startMenu(self, selection):
        try:
            if selection == "exit":
                self.EXIT = True
                return
            for i, item in enumerate(self.MENU):
                if i == selection:
                    print(f"Selected: {item}")
                    build_data = item.get("build", {})
                    path = build_data.get("path")
                    action = build_data.get("action")
                    source = build_data.get("source")
                    method = build_data.get("method")
                    if method is None:
                        method = "mods"
                    
                    if path and action and source:
                        full_path = os.path.join("data", "lib", method, path, source) # data/lib/str: method/str: path/str: sourcepool
                        print(f"Loading action from: {full_path}")
                        
                        if os.path.isfile(full_path):
                            # Sauberer Import mit importlib
                            self.ClearConsole()
                            import importlib.util
                            spec = importlib.util.spec_from_file_location("mod", full_path)
                            mod = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(mod)
                            
                            if hasattr(mod, action):
                                getattr(mod, action)()
                                print(f"Successfully executed {action}()")
                            else:
                                print(f"Function '{action}' not found in {full_path}")
                        else:
                            print(f"Action file not found: {full_path}")
                        break
                    else:
                        print("Invalid menu item configuration - missing path, action, or source.")
                        break
        except Exception as e:
            print(f"Error executing menu action: {e}")
            import traceback
            traceback.print_exc()
    
    def ClearTempFiles(self):
        """Löscht alle Ordner und Dateien im temp (tmp) Ordner"""
        import shutil
        temp_path = self.TEMPPATH
        
        try:
            if os.path.exists(temp_path):
                # Alle Inhalte des tmp Ordners löschen
                for item in os.listdir(temp_path):
                    item_path = os.path.join(temp_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Ordner rekursiv löschen
                        print(f"🗑️ Ordner gelöscht: {item_path}")
                    elif os.path.isfile(item_path):
                        os.remove(item_path)  # Datei löschen
                        print(f"🗑️ Datei gelöscht: {item_path}")
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Leeren des Temp-Ordners: {e}")
            return False