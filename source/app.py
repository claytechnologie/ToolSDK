import modules.engine as engine
import os


class App(engine.Engine):    
    
    def __init__(self, settings_path=None):
        if settings_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            settings_path = os.path.join(project_root, "data", "assets", "manager", "settings.json")
        super().__init__(settings_path=settings_path)
        self.isRunning = False
        self.BuildMainMenu()  # Menu erstellen
        self.END = False
        self.task = None
    
    def BuildMainMenu(self):
        """Erstellt das Hauptmenü mit aktuellen Übersetzungen"""
        mainmenu = [{"build": {
                    "mesh": self.Language.Translate("settings"),
                    "source": "settings.py",
                    "action": "main",
                    "path": "settings",
                    "method": "main" 
                }}, {
                    "build": {
                    "mesh": self.Language.Translate("book"),
                    "source": "book.py",
                    "action": "start",
                    "path": "book",
                    "method": "main"
                }
                    },
                {
                    "build": {
                    "mesh": self.Language.Translate("package_management"),
                    "source": "package.py",
                    "action": "start",
                    "path": "packages",
                    "method": "package"
                }
                    }]
        # Menu komplett neu setzen, nicht anhängen
        self.menu.MENU = mainmenu.copy()
        
        # Mods laden wenn aktiviert
        if self.menu.mods_enabled:
            self.menu.LoadModMenus(self.loader)
    
    def run(self):
        print(self.Language.Translate("app_is_running"))
        self.isRunning = True

        
        
        while self.isRunning:
            
            if self.StateMachine.IsState(self.StateMachine.FIRST_ENTRY):
                self.menu.ShowPossibleErrors()    
                self.menu.ClearConsole() 
                self.menu.ShowHeader()
                self.menu.ReadMenuData()
                self.menu.ShowMenu()
                
            self.StateMachine.SetState(self.StateMachine.MAINMENU)
            self.Temp.RemoveTempFile()

            if self.Settings.CheckIfUpdate():
                self.Settings.Update()
                self.Language.Reload()
                self.BuildMainMenu()
                self.menu.ReadMenuData()
                print(self.Language.Translate("setting_changed"))

            if self.StateMachine.IsState(self.StateMachine.MAINMENU):
                self.menu.ClearConsole()
                self.menu.ShowHeader()
                self.menu.ShowMenu()


            if self.StateMachine.IsState(self.StateMachine.EXIT):
                print(self.Language.Translate("exiting_app"))
                self.isRunning = False
                break

            self.doTasks()
      
    def doTasks(self):
        try:
            print()
            self.menu.DoMenuSelection(int(input(self.Language.Translate("input"))))
        except ValueError:
            print(self.Language.Translate("invalid_option"))
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
        print(app.Language.Translate("ask_exit"))
        confirm = input()
        if confirm == "":
            print("Exiting application...")
            exit(0)
        else:
            app.run()
if __name__ == "__main__":
    main()