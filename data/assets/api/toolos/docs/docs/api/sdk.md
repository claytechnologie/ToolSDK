# Modding SDK

Erstelle deine eigenen Mods und Erweiterungen für ToolOS-basierte Anwendungen!

## 🎮 Was sind Mods?

Mods sind eigenständige Module, die in ToolOS-Apps geladen werden können. Sie erweitern die Funktionalität ohne den Kern-Code zu ändern.

### Beispiel: Shopping Mod aus deiner Codebase
```python
import toolos as engine

class ModdedApp(engine.ToolsApi):

    def __init__(self):
        super().__init__("settings.json", **sdk) # Requires sdk dict (see below)
        self.SDK = sdk
        self.AppName = sdk.get("name")
        self.Version = sdk.get("version")
        
        # Initialisiere Logging
        self.Log.CreateLogFile("modded_app.log")
        self.Log.WriteLog("modded_app.log", f"{self.AppName} v{self.Version} started")
        
    def ShowMainMenu(self):
        print(self.Language.Translate("header"))
        print(f"1. {self.Language.Translate('new_shopping')}")
        print(f"2. {self.Language.Translate('exit')}")
        
        choice = input(self.Language.Translate("input"))
        if choice == "0":
            self.StartShopping()
        elif choice == "1":
            self.StateMachine.SetState("exit")
            
    def StartShopping(self):
        # Einkaufslogik mit State Management
        self.StateMachine.SetState("shopping_mode")
        # Speichere Einkaufssession im Cache
        session_data = {"items": [], "total": 0.0}
        self.Cache.WriteCacheFile("current_session.json", 
                                json.dumps(session_data))
```

## 📁 Mod-Struktur

```
MyMod/
├── package.json          # Mod-Informationen
├── data/
│   └── lang/            # Übersetzungen
│       ├── de.json
│       ├── en.json
│       └── ...
└── src/
    ├── app.py           # Haupt-Mod-Datei
    └── engine/
        └── engine.py    # Mod-Engine (optional)
```

## 📋 package.json

```json
{
    "name": "Shopping Simulator",
    "version": "2.0.4",
    "author": "Your Name",
    "description": "A realistic shopping experience simulator",
    "main": "src/app.py",
    "languages": ["de", "en", "fr", "es"],
    "dependencies": [],
    "type": "mod"
}
```

## 🌍 Multi-Language Support

### Übersetzungsdateien

**data/lang/de.json:**
```json
{
    "header": "=== Shopping Simulator ===",
    "new_shopping": "Neuer Einkauf",
    "shopping_cart": "Warenkorb",
    "total_price": "Gesamtpreis",
    "checkout": "Zur Kasse",
    "exit": "Beenden",
    "input": "Eingabe: > "
}
```

**data/lang/en.json:**
```json
{
    "header": "=== Shopping Simulator ===",
    "new_shopping": "New Shopping",
    "shopping_cart": "Shopping Cart", 
    "total_price": "Total Price",
    "checkout": "Checkout",
    "exit": "Exit",
    "input": "Input: > "
}
```

### Sprachen in Mods laden

```python
class ShoppingApp():
    def __init__(self, api):
        self.api = api
        self.language = api.Language
        
        # Lade Mod-spezifische Übersetzungen
        self.LoadModLanguages()
        
    def LoadModLanguages(self):
        import os
        lang_path = os.path.join(os.path.dirname(__file__), "../data/lang")
        current_lang = self.api.Settings.LANGUAGE
        
        lang_file = os.path.join(lang_path, f"{current_lang}.json")
        if os.path.exists(lang_file):
            self.language.AddLanguagePackage(current_lang, lang_file)
            self.language.Reload()
```

## 🔧 Mod-Engine erstellen

Für komplexere Mods kannst du eine eigene Engine erstellen:

```python
# src/engine/engine.py
import toolos as base_engine

class ModEngine(base_engine.Api):
    def __init__(self, settings_path):
        super().__init__(settings_path)
        self.ModName = "Shopping Simulator"
        self.ModVersion = "2.0.4"
        
    def InitializeMod(self):
        """Mod-spezifische Initialisierung"""
        self.Log.WriteLog("mod.log", f"{self.ModName} v{self.ModVersion} loaded")
        
        # Lade Mod-Konfiguration
        if self.Cache.CacheExists("mod_config.json"):
            import json
            config_data = self.Cache.ReadCacheFile("mod_config.json")
            self.ModConfig = json.loads(config_data)
        else:
            self.CreateDefaultConfig()
            
    def CreateDefaultConfig(self):
        """Erstelle Standard-Mod-Konfiguration"""
        import json
        default_config = {
            "difficulty": "normal",
            "currency": "EUR",
            "shop_items": 50,
            "enable_discounts": True
        }
        
        config_data = json.dumps(default_config, indent=2)
        self.Cache.WriteCacheFile("mod_config.json", config_data)
        self.ModConfig = default_config
```

## 🎯 State Management in Mods

```python
class ShoppingStates:
    SHOPPING_MENU = "shopping_menu"
    BROWSING_ITEMS = "browsing_items"
    IN_CART = "in_cart"
    CHECKOUT = "checkout"
    PAYMENT = "payment"

class ShoppingMod(ModEngine):
    def __init__(self):
        super().__init__("settings.json")
        self.States = ShoppingStates()
        self.ShoppingCart = []
        self.TotalPrice = 0.0
        
    def Run(self):
        self.StateMachine.SetState(self.States.SHOPPING_MENU)
        
        while True:
            if self.StateMachine.IsState(self.States.SHOPPING_MENU):
                self.ShowShoppingMenu()
            elif self.StateMachine.IsState(self.States.BROWSING_ITEMS):
                self.BrowseItems()
            elif self.StateMachine.IsState(self.States.CHECKOUT):
                self.ProcessCheckout()
            elif self.StateMachine.IsState(self.StateMachine.EXIT):
                break
```

## 💾 Mod-Daten verwalten

```python
class ShoppingData:
    def __init__(self, mod_engine):
        self.engine = mod_engine
        
    def SaveShoppingSession(self, cart_items, total):
        """Speichere Einkaufssession"""
        import json
        session_data = {
            "timestamp": self.GetCurrentTimestamp(),
            "items": cart_items,
            "total": total,
            "currency": self.engine.ModConfig.get("currency", "EUR")
        }
        
        filename = f"shopping_session_{session_data['timestamp']}.json"
        self.engine.Cache.WriteCacheFile(filename, json.dumps(session_data, indent=2))
        self.engine.Log.WriteLog("shopping.log", f"Session saved: {total} {session_data['currency']}")
        
    def LoadShoppingSessions(self):
        """Lade alle Einkaufssessions"""
        sessions = []
        # Implementierung zum Laden aller Session-Files
        return sessions
        
    def GetCurrentTimestamp(self):
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
```

## 🚀 Mod-Loading System

So lädt die Haupt-App deine Mods:

```python
# Im Haupt-App Loader
class ModLoader:
    def __init__(self, settings):
        self.settings = settings
        self.LoadedMods = []
        
    def LoadMods(self):
        import os
        import json
        
        mod_path = self.settings.Global("modpath")
        if not os.path.exists(mod_path):
            return
            
        for mod_folder in os.listdir(mod_path):
            package_file = os.path.join(mod_path, mod_folder, "package.json")
            if os.path.exists(package_file):
                with open(package_file, 'r', encoding='utf-8') as f:
                    mod_info = json.load(f)
                    
                self.LoadMod(mod_folder, mod_info)
                
    def LoadMod(self, folder_name, mod_info):
        """Lade einzelnen Mod"""
        mod_entry = {
            "build": {
                "mesh": f"{mod_info['name']} v{mod_info['version']}",
                "source": mod_info["main"],
                "action": "start",
                "path": folder_name,
                "method": "main"
            }
        }
        self.LoadedMods.append(mod_entry)
```

## 📚 Mod-Beispiele

### 1. Terminal Mod
```python
# Einfacher Terminal-Emulator
class TerminalMod(ModEngine):
    def RunCommand(self, command):
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
```

### 2. Task Manager Mod  
```python
# Aufgabenverwaltung
class TaskManagerMod(ModEngine):
    def AddTask(self, title, priority="normal"):
        task = {
            "id": self.GenerateTaskId(),
            "title": title,
            "priority": priority,
            "created": self.GetCurrentTimestamp(),
            "completed": False
        }
        self.SaveTask(task)
```

## 🛠️ Best Practices für Mods

1. **Eigene Language Packages**: Nutze das Multi-Language-System
2. **State Management**: Verwende die StateMachine für sauberen Flow
3. **Daten persistieren**: Nutze Cache/Temp APIs für Mod-Daten
4. **Logging**: Protokolliere wichtige Mod-Events
5. **Fehlerbehandlung**: Robuste Error-Handling-Implementierung
6. **Konfigurierbar**: Lade Mod-Settings aus JSON-Files
7. **Performance**: Effiziente Datenstrukturen verwenden

## 🎉 Mod veröffentlichen

1. **Testen**: Ausgiebig in verschiedenen Sprachen testen
2. **Dokumentation**: README mit Installation und Usage
3. **Versionierung**: Semantische Versionierung verwenden
4. **Package.json**: Vollständige Mod-Informationen
5. **Beispiele**: Code-Beispiele für andere Entwickler