class SettingsManager:
    
    def __init__(self):
        import json as js
        self.js = js
        self.IsRUNNING = True
        self.SETTINGSPATH = "data/assets/manager/settings.json"
        
    def LoadSettings(self):
        with open (self.SETTINGSPATH, "r", encoding="utf-8") as f:
            self.SETTINGS = self.js.load(f)
            return True
        return False
    
    def ShowSettings(self):
        for key, value in enumerate(self.SETTINGS.items()):
            print(f"{key}: {value[0]} = {value[1]}")
        return True
    
    def EditSettings(self, key, value):
        for k, v in enumerate(self.SETTINGS.items()):
            if k == key:
                self.SETTINGS[v[0]] = value
                self.SETTINGS["update"] = True
                print("Settings aktualisiert:", self.SETTINGS)
                self.js.dump(self.SETTINGS, open(self.SETTINGSPATH, "w", encoding="utf-8"), indent=4)
                print(f"Setting '{v[0]}' auf '{value}' gesetzt.")
                
                return True
            
    def AskInput(self, text):
       eingabe = input(f"{text}: ")
       return eingabe

    
def main():
    sm = SettingsManager()
    sm.LoadSettings()
    while sm.IsRUNNING:
        print("\nSettings Manager")
        print()
        sm.ShowSettings()
        eingabe = sm.AskInput("Eingabe (q zum beenden)> ")
        if eingabe.lower() == 'q': 
            sm.IsRUNNING = False
            print("Beende Settings Manager...")
            break
        else:
            try:
                key = int(eingabe)
                value = sm.AskInput("Neuer Wert> ")
                sm.EditSettings(key, value)
            except IndexError:
                print("Ungültiger Key.")
                
                

main()