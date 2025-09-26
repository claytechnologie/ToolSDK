# API Reference

Vollständige API-Referenz für alle ToolOS SDK Komponenten.

## 🏗️ Engine.Api (Base Class)

| Komponente | Typ | Beschreibung | Verfügbare Methoden |
|------------|-----|--------------|-------------------|
| `self.Settings` | ToolOS.Settings | Einstellungsverwaltung | `Global()`, `User()`, `Save()`, `LoadSettings()` |
| `self.Language` | ToolOS.Language | Multi-Language-System | `Translate()`, `SetLanguage()`, `AddLanguagePackage()` |
| `self.Cache` | ToolOS.Cache | Cache-Management | `WriteCacheFile()`, `ReadCacheFile()`, `CacheExists()` |
| `self.StateMachine` | ToolOS.StateMachine | State-Management | `SetState()`, `GetState()`, `IsState()` |
| `self.Temp` | ToolOS.Temp | Temporäre Dateien | `WriteTempFile()`, `ReadTempFile()`, `TempExists()` |
| `self.Log` | ToolOS.Log | Logging-System | `WriteLog()`, `ReadLog()`, `CreateLogFile()` |
| `self.Package` | ToolOS.Package | Package-Management | `LoadPackage()`, `GetPackageInfo()`, `ListPackages()` |

## ⚙️ Settings API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `Global(key)` | `key: str` | `str` | Globale Einstellung abrufen |
| `User(key)` | `key: str` | `str` | Benutzer-Einstellung abrufen |
| `Save()` | - | `bool` | Einstellungen speichern |
| `LoadSettings()` | - | `dict` | Alle Einstellungen laden |
| `SetGlobal(key, value)` | `key: str, value: str` | `bool` | Globale Einstellung setzen |
| `SetUser(key, value)` | `key: str, value: str` | `bool` | Benutzer-Einstellung setzen |

### Settings Beispiele

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Einstellungen abrufen
        language = self.Settings.Global("language")
        user_theme = self.Settings.User("theme")
        
        # Einstellungen setzen
        self.Settings.SetGlobal("app_version", "1.0.0")
        self.Settings.SetUser("last_login", "2024-01-01")
        self.Settings.Save()
```

## 🌍 Language API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `Translate(key)` | `key: str` | `str` | Text übersetzen |
| `SetLanguage(lang)` | `lang: str` | `bool` | Sprache wechseln |
| `AddLanguagePackage(lang, file_path)` | `lang: str, file_path: str` | `bool` | Sprachpaket hinzufügen |
| `GetAvailableLanguages()` | - | `list` | Verfügbare Sprachen |
| `GetCurrentLanguage()` | - | `str` | Aktuelle Sprache |
| `Reload()` | - | `bool` | Sprachpakete neu laden |

### Language Beispiele

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Text übersetzen
        welcome_text = self.Language.Translate("welcome")
        menu_title = self.Language.Translate("main_menu")
        
        # Sprache wechseln
        self.Language.SetLanguage("en")
        
        # Verfügbare Sprachen anzeigen
        languages = self.Language.GetAvailableLanguages()
        print(f"Verfügbare Sprachen: {languages}")
```

## 💾 Cache API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `WriteCacheFile(filename, data)` | `filename: str, data: str` | `bool` | Cache-Datei schreiben |
| `ReadCacheFile(filename)` | `filename: str` | `str` | Cache-Datei lesen |
| `CacheExists(filename)` | `filename: str` | `bool` | Cache-Datei existiert |
| `DeleteCacheFile(filename)` | `filename: str` | `bool` | Cache-Datei löschen |
| `ListCacheFiles()` | - | `list` | Alle Cache-Dateien |
| `ClearCache()` | - | `bool` | Cache komplett leeren |

### Cache Beispiele

```python
import toolos as engine
import json

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Daten cachen
        user_data = {"name": "John", "score": 1500}
        self.Cache.WriteCacheFile("user_data.json", json.dumps(user_data))
        
        # Daten aus Cache laden
        if self.Cache.CacheExists("user_data.json"):
            cached_data = self.Cache.ReadCacheFile("user_data.json")
            user_data = json.loads(cached_data)
            print(f"Benutzername: {user_data['name']}")
```

## 🔄 StateMachine API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `SetState(state)` | `state: str` | `bool` | Zustand setzen |
| `GetState()` | - | `str` | Aktuellen Zustand abrufen |
| `IsState(state)` | `state: str` | `bool` | Zustand prüfen |
| `PreviousState()` | - | `str` | Vorherigen Zustand abrufen |
| `StateHistory()` | - | `list` | State-Historie |
| `ResetState()` | - | `bool` | Zustand zurücksetzen |

### StateMachine Beispiele

```python
import toolos as engine

class AppStates:
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    GAME = "game"
    EXIT = "exit"

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.States = AppStates()
        
    def Run(self):
        self.StateMachine.SetState(self.States.MAIN_MENU)
        
        while True:
            current_state = self.StateMachine.GetState()
            
            if self.StateMachine.IsState(self.States.MAIN_MENU):
                self.ShowMainMenu()
            elif self.StateMachine.IsState(self.States.SETTINGS):
                self.ShowSettings()
            elif self.StateMachine.IsState(self.States.EXIT):
                break
```

## 📄 Temp API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `WriteTempFile(filename, data)` | `filename: str, data: str` | `bool` | Temp-Datei schreiben |
| `ReadTempFile(filename)` | `filename: str` | `str` | Temp-Datei lesen |
| `TempExists(filename)` | `filename: str` | `bool` | Temp-Datei existiert |
| `DeleteTempFile(filename)` | `filename: str` | `bool` | Temp-Datei löschen |
| `ListTempFiles()` | - | `list` | Alle Temp-Dateien |
| `ClearTemp()` | - | `bool` | Temp-Ordner leeren |

### Temp Beispiele

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Temporäre Datei erstellen
        temp_data = "Temporäre Verarbeitungsdaten"
        self.Temp.WriteTempFile("processing.txt", temp_data)
        
        # Temporäre Datei verarbeiten
        if self.Temp.TempExists("processing.txt"):
            data = self.Temp.ReadTempFile("processing.txt")
            # Verarbeitung...
            self.Temp.DeleteTempFile("processing.txt")
```

## 📝 Log API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `WriteLog(filename, message)` | `filename: str, message: str` | `bool` | Log-Eintrag schreiben |
| `ReadLog(filename)` | `filename: str` | `str` | Log-Datei lesen |
| `CreateLogFile(filename)` | `filename: str` | `bool` | Log-Datei erstellen |
| `LogExists(filename)` | `filename: str` | `bool` | Log-Datei existiert |
| `ClearLog(filename)` | `filename: str` | `bool` | Log-Datei leeren |
| `ListLogFiles()` | - | `list` | Alle Log-Dateien |

### Log Beispiele

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Logging initialisieren
        self.Log.CreateLogFile("app.log")
        
        # Log-Einträge schreiben
        self.Log.WriteLog("app.log", "Application started")
        self.Log.WriteLog("app.log", "User logged in")
        self.Log.WriteLog("error.log", "Database connection failed")
        
        # Logs auslesen
        app_logs = self.Log.ReadLog("app.log")
        print("App Logs:", app_logs)
```

## 📦 Package API

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `LoadPackage(package_name)` | `package_name: str` | `object` | Package laden |
| `GetPackageInfo(package_name)` | `package_name: str` | `dict` | Package-Informationen |
| `ListPackages()` | - | `list` | Alle Packages |
| `PackageExists(package_name)` | `package_name: str` | `bool` | Package existiert |
| `ReloadPackage(package_name)` | `package_name: str` | `bool` | Package neu laden |
| `UnloadPackage(package_name)` | `package_name: str` | `bool` | Package entladen |

### Package Beispiele

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Package laden
        shopping_mod = self.Package.LoadPackage("Shopping")
        task_manager = self.Package.LoadPackage("TaskManager")
        
        # Package-Informationen abrufen
        package_info = self.Package.GetPackageInfo("Shopping")
        print(f"Package: {package_info['name']} v{package_info['version']}")
        
        # Alle verfügbaren Packages
        packages = self.Package.ListPackages()
        for package in packages:
            print(f"- {package}")
```

## 🚀 Vollständiges App-Beispiel

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # App-spezifische Initialisierung
        self.AppName = "My ToolOS App"
        self.Version = "1.0.0"
        
        # Logging initialisieren
        self.Log.CreateLogFile("app.log")
        self.Log.WriteLog("app.log", f"{self.AppName} v{self.Version} started")
        
        # Standard-Konfiguration laden/erstellen
        self.InitializeConfig()
        
    def InitializeConfig(self):
        """App-Konfiguration initialisieren"""
        if not self.Cache.CacheExists("app_config.json"):
            import json
            default_config = {
                "theme": "dark",
                "auto_save": True,
                "notifications": True
            }
            self.Cache.WriteCacheFile("app_config.json", json.dumps(default_config))
            
    def Run(self):
        """Haupt-App-Loop"""
        while True:
            if self.StateMachine.IsState("main_menu"):
                self.ShowMainMenu()
            elif self.StateMachine.IsState("exit"):
                self.Cleanup()
                break
                
    def ShowMainMenu(self):
        """Hauptmenü anzeigen"""
        print(self.Language.Translate("welcome"))
        # Menu-Logik...
        
    def Cleanup(self):
        """App beenden und aufräumen"""
        self.Log.WriteLog("app.log", f"{self.AppName} shutting down")
        self.Temp.ClearTemp()  # Temporäre Dateien löschen
        
if __name__ == "__main__":
    app = MyApp()
    app.Run()
```

## 🎯 Error Handling

```python
import toolos as engine

class MyApp(engine.Api):
    def SafeOperation(self):
        try:
            # Kritische Operation
            data = self.Cache.ReadCacheFile("important_data.json")
            result = self.ProcessData(data)
            return result
            
        except FileNotFoundError:
            self.Log.WriteLog("error.log", "Important data file not found")
            return None
            
        except Exception as e:
            self.Log.WriteLog("error.log", f"Unexpected error: {str(e)}")
            return None
            
    def ProcessData(self, data):
        # Datenverarbeitung
        pass
```

## 📊 Performance Tips

1. **Cache nutzen**: Häufig verwendete Daten cachen
2. **Logs optimieren**: Nicht zu detailliert loggen
3. **Temp Files**: Große Daten temporär speichern
4. **State Management**: Saubere State-Übergänge
5. **Language Loading**: Sprachen nur bei Bedarf laden
6. **Package Loading**: Packages lazy laden