import os

class MenuAsset:
    
    def __init__(self, api):
        self.api = api
        self.Update()
        self.HEADER: str = None
        self.MENU: list = None
        self.EXIT = False
        self.dMENU = []
        self.ERRORS = None
        self.RELOAD = False
        self.TEMPPATH = None
    
    
    def ClearConsole(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        

        
        
    def ShowHeader(self, header=None):
        if header:
            print("----------------------")
            print(header)
            print("----------------------")
            print()
        else:
            print("----------------------")
            print(self.api.Language.Translate("header"))
            print("----------------------")
            print()
            
    def ReadMenuData(self):
        self.dMENU.clear()  # Menu-Cache leeren bevor neue Daten gelesen werden
        for item in self.MENU:
                self.dMENU.append(item.get("build", {}).get('mesh'))
            
    def ShowMenu(self, menu: list = None, action=None):
        if self.dMENU and menu is None:
            for i, name in enumerate(self.dMENU):
                print(i, name)
        elif menu is not None:
            for i, name in enumerate(menu):
                print(i, name)
            if action == 0:
                self.dMENU = menu
        else:
            self.api.Language.Translate("no_menu_data")
                
            
            
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
        
    def Update(self):
        
        self.HEADER = self.api.Settings.Global("header") if self.api.Settings.Global("header") else None
        self.ERRORS = self.api.Settings.Global("errors") if self.api.Settings.Global("errors") else None
        self.mods_enabled = self.api.Settings.Global("mods_enabled") if self.api.Settings.Global("mods_enabled") else False
        self.INPUTNAME = self.api.Settings.Global("inputname") if self.api.Settings.Global("inputname") else None
        self.VERSION = self.api.Settings.Global("version") if self.api.Settings.Global("version") else None
        self.LANGUAGE = self.api.Settings.Global("language") if self.api.Settings.Global("language") else None
        self.TEMPPATH = self.api.Settings.Global("temppath") if self.api.Settings.Global("temppath") else None
        
        
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
