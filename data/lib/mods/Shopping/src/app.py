import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_path)
import engine.engine as engine


    #? #################  MENU #####################

class Menu():
    
    def __init__(self, app):
        self.app = app
        self.MENU = [self.app.language.Translate("new_shopping"), self.app.language.Translate("exit")]
        self.ShowHeader()


    def ShowHeader(self):
        print(self.app.language.Translate("header"))
        print()


    def ShowMainMenu(self):
        self.app.state.SetNewState(self.app.state.types.MAIN_MENU)
        for i, key in enumerate(self.MENU):
            print(f"{i}. {key}")
        print()
        choice = input(self.app.language.Translate("input"))
        for i, key in enumerate(self.MENU):
            if choice == str(i):
                if key == self.app.language.Translate("exit"):
                    self.app.isRunning = False
                    self.app.api.state.SetState(self.app.api.state.EXIT)
                    
                elif key == self.app.language.Translate("new_shopping"):
                    self.app.state.SetState("shopping")

    #? #################  App #####################


class ShoppingApp(engine.Engine):


    def __init__(self, sdk, package: dict, caller):
        # Initialize the Engine for Modding
        super().__init__(sdk=sdk, package=package) # Automaticly loads Sdk & package from package.json
        
        # Variables
        self.PREFERRED_LANGUAGE = self.api.Settings.LANGUAGE
        self.isRunning = False
        
        # Language API
        self.api.language.AddLanguagePackage(language="de", datapath="data/lib/mods/Shopping/data/lang/de.json")
        self.api.language.AddLanguagePackage(language="en", datapath="data/lib/mods/Shopping/data/lang/en.json")
        self.api.language.AddLanguagePackage(language="ru", datapath="data/lib/mods/Shopping/data/lang/ru.json")
        self.api.language.Reload()
        
        # State Machine
        self.state = self.api.state_machine
        
        # Imports
        self.main = caller
        
        
    def run(self):
        self.isRunning = True
        self.menu = Menu(self)
        
        while self.isRunning:
            
            #? Main Menu Logic
            if self.state.GetState() == self.state.MAINMENU:
                self.menu.ShowMainMenu()

            elif self.state.GetState() == self.state.STEP_1:
                print(self.api.language.Translate("new_shopping") + " - " + self.api.language.Translate("not_implemented"))
                self.state.SetNewState(self.state.MAINMENU)

            elif self.state.GetState() == self.state.EXIT:
                self.isRunning = False
                print(self.api.language.Translate("exiting_app"))
    
    def ShowWelcome(self):
        print(self.api.language.Translate("welcome"))


    #? #################  START #####################


class Start:
    
    
    def __init__(self):
        import json
        with open('data/lib/mods/Shopping/package.json', 'r') as f:
            package = json.load(f)

        version = package['build'].get('sdk', {}).get('version', '')
        name = package['build'].get('sdk', {}).get('name', '')
        sdk = {
            "name": name,
            "version": version
        }
        package = package['build'].get('sdk', {}).get('package', {})
        self.App = ShoppingApp(sdk=sdk, package=package, caller=self)
        self.App.run()
        self.API = self.App
        self.Configure = self.ConfigureAPI()
      
      
        
    def ConfigureAPI(self):
        return self.API


    #? #################  Mod EntryPoint #####################
    
    
def main():
    try:
        app = Start()
    except Exception as e:
        raise TypeError("Fehler beim Starten der Shopping-App:", e)
    except KeyboardInterrupt:
        print("\nHardexiting via KeyboardInterrupt")
        exit(0)
    
        
    #? #################  Testing #####################


if __name__ == "__main__":
    app = Start()
    app.API.ShowWelcome()
    state = app.API.state.GetState()
    print("Current State:", state)