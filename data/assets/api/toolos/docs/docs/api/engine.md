# Engine API

Die Engine API ist deine Basis-Klasse für ToolOS-Anwendungen. Einfach erben und loslegen!

## Der Vererbungsansatz

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        # Alle APIs sind jetzt verfügbar als self.Language, self.Cache, etc.
        
    def Run(self):
        # Deine App-Logik hier
        pass
```

## Verfügbare Properties

Nach der Vererbung hast du Zugriff auf alle ToolOS APIs:

| Property | Type | Beschreibung |
|----------|------|--------------|
| `self.Settings` | SettingsAPI | Konfigurationsverwaltung |
| `self.Language` | LanguageAPI | Multi-Language Support |
| `self.Cache` | CacheAPI | Datei-Caching System |
| `self.StateMachine` | StateMachineAPI | State Management |
| `self.Temp` | TempAPI | Temporäre Dateien |
| `self.Log` | LogAPI | Logging System |
| `self.Package` | PackageAPI | Mod/Package Management |
| `self.Helper` | HelperAPI | Utility Functions |

## Beispiel: Komplette App

```python
import toolos as engine

class TaskManager(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.isRunning = False
        self.tasks = []
        
    def Run(self):
        self.LoadTasks()
        print(self.Language.Translate("welcome"))
        self.isRunning = True
        
        while self.isRunning:
            if self.StateMachine.IsState(self.StateMachine.MAINMENU):
                self.ShowMainMenu()
            elif self.StateMachine.IsState(self.StateMachine.EXIT):
                break
                
    def LoadTasks(self):
        if self.Cache.CacheExists("tasks.json"):
            import json
            data = self.Cache.ReadCacheFile("tasks.json")
            self.tasks = json.loads(data)
            self.Log.WriteLog("app.log", f"Loaded {len(self.tasks)} tasks")
            
    def ShowMainMenu(self):
        print("\n=== " + self.Language.Translate("task_manager") + " ===")
        print("1. " + self.Language.Translate("add_task"))
        print("2. " + self.Language.Translate("list_tasks"))
        print("3. " + self.Language.Translate("exit"))
        
        choice = input(self.Language.Translate("input"))
        
        if choice == "1":
            self.AddTask()
        elif choice == "2":
            self.ListTasks()
        elif choice == "3":
            self.StateMachine.SetState(self.StateMachine.EXIT)
            
    def AddTask(self):
        title = input(self.Language.Translate("enter_task_title"))
        task = {"id": len(self.tasks) + 1, "title": title, "done": False}
        self.tasks.append(task)
        self.SaveTasks()
        print(self.Language.Translate("task_added"))
        
    def SaveTasks(self):
        import json
        data = json.dumps(self.tasks, indent=2)
        self.Cache.WriteCacheFile("tasks.json", data)
        self.Log.WriteLog("app.log", "Tasks saved")

if __name__ == "__main__":
    app = TaskManager()
    app.Run()
```

## Best Practices

1. **Immer super().__init__() aufrufen**: Initialisiert alle APIs
2. **CamelCase für Methoden**: `ShowMainMenu()`, `LoadTasks()`
3. **Properties nutzen**: `self.Language.Translate()` statt direkte API-Calls
4. **State Machine verwenden**: Saubere App-Flow-Kontrolle
5. **Logging einbauen**: Für Debugging und Monitoring

## Warum Vererbung?

- ✅ **Sauberer Code**: Alle APIs direkt verfügbar
- ✅ **Einfache Struktur**: Eine Klasse, alles drin
- ✅ **Menschlich lesbar**: Kein kompliziertes API-Handling
- ✅ **Erweiterbar**: Einfach neue Methoden hinzufügen
- ✅ **Testbar**: Klare Klassenstruktur