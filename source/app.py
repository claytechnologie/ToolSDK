import modules.engine as engine


class App(engine.Engine):    
    
    def __init__(self):
        super().__init__()
        self.menu.SetSettings(self.settings)
        self.isRunning = False
        mainmenu = [{"build": {
                    "mesh": self.lang.SETTINGS,
                    "source": "settings.py",
                    "action": "main",
                    "path": "settings",
                    "method": "main" # Method is the Call of a __serial__.main() in the lib/ folder so its basicly [ lib/main ]
                }}, {
                    "build": {
                    "mesh": self.lang.DIARY,
                    "source": "book.py",
                    "action": "start",
                    "path": "book",
                    "method": "main"
                }
                    },
                {
                    "build": {
                    "mesh": self.lang.PACKAGE_MANAGEMENT,
                    "source": "package.py",
                    "action": "start",
                    "path": "packages",
                    "method": "package"
                }
                    }]
        self.menu.MENU = mainmenu
        self.END = False
        self.task = None
    
    def run(self):
        
        print(self.lang.APP_RUNNING)
        self.isRunning = True

        if self.menu.mods_enabled:
            self.menu.LoadModMenus(self.loader)
            
        self.menu.ShowPossibleErrors()    
        self.menu.ClearConsole()
        self.menu.ShowHeader()
        self.menu.ReadMenuData()
        self.menu.ShowMenu()
        
        
        while self.isRunning:
            self.menu.ClearTempFiles()

            if self.settings.CheckIfUpdate():
                self.menu.RELOAD = True
                print(self.lang.SETTINGS_CHANGED)
                if self.settings.MODS_ENABLED:
                    self.menu.LoadModMenus(self.loader)
                self.menu.ReloadMenu(self.settings)
            
            if self.menu.EXIT:
                print(self.lang.EXIT_SELECTED)
                self.isRunning = False
                print(self.lang.EXITING_APP)
                break
            self.menu.ClearConsole()
            self.menu.ShowHeader()
            self.menu.ShowMenu()

            self.doTasks()
      
    def doTasks(self):
        try:
            print()
            self.menu.DoMenuSelection(int(input(self.lang.INPUT_PROMPT)))
        except ValueError:
            print(self.lang.INVALID_OPTION)
            self.task = None
            
    def checkEnd(self):
        if self.menu.EXIT:
            return True
        return False
def main():
    app = App()
    try:
        app.run()
    except KeyboardInterrupt:
        print(app.lang.ASK_EXIT)
        confirm = input()
        if confirm == "":
            print("Exiting application...")
            exit(0)
        else:
            app.run()
if __name__ == "__main__":
    main()