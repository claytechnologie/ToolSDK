# Modding SDK

Create your own mods and extensions for ToolOS-based applications!

## 🎮 What are Mods?

Mods are standalone modules that can be loaded into ToolOS apps. They extend functionality without modifying core code.

### Example: Shopping Mod from your Codebase

```python
import sys
import os
src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_path)
import engine.engine as engine

class Menu():
    def __init__(self, app):
        self.app = app
        self.MENU = [
            self.app.language.Translate("new_shopping"), 
            self.app.language.Translate("exit")
        ]
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
                if i == 0:  # New Shopping
                    self.StartShopping()
                elif i == 1:  # Exit
                    self.app.state.SetNewState(self.app.state.types.EXIT)
```

## 📁 Mod Structure

```
MyMod/
├── package.json          # Mod information
├── data/
│   └── lang/            # Translations
│       ├── de.json
│       ├── en.json
│       └── ...
└── src/
    ├── app.py           # Main mod file
    └── engine/
        └── engine.py    # Mod engine (optional)
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

### Translation Files

**data/lang/de.json:**
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

### Loading Languages in Mods

```python
class ShoppingApp():
    def __init__(self, api):
        self.api = api
        self.language = api.Language
        
        # Load mod-specific translations
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

## 🔧 Creating Mod Engine

For complex mods, you can create your own engine:

```python
# src/engine/engine.py
import toolos as base_engine

class ModEngine(base_engine.Api):
    def __init__(self, settings_path):
        super().__init__(settings_path)
        self.ModName = "Shopping Simulator"
        self.ModVersion = "2.0.4"
        
    def InitializeMod(self):
        """Mod-specific initialization"""
        self.Log.WriteLog("mod.log", f"{self.ModName} v{self.ModVersion} loaded")
        
        # Load mod configuration
        if self.Cache.CacheExists("mod_config.json"):
            import json
            config_data = self.Cache.ReadCacheFile("mod_config.json")
            self.ModConfig = json.loads(config_data)
        else:
            self.CreateDefaultConfig()
            
    def CreateDefaultConfig(self):
        """Create default mod configuration"""
        import json
        default_config = {
            "difficulty": "normal",
            "currency": "USD",
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

## 💾 Managing Mod Data

```python
class ShoppingData:
    def __init__(self, mod_engine):
        self.engine = mod_engine
        
    def SaveShoppingSession(self, cart_items, total):
        """Save shopping session"""
        import json
        session_data = {
            "timestamp": self.GetCurrentTimestamp(),
            "items": cart_items,
            "total": total,
            "currency": self.engine.ModConfig.get("currency", "USD")
        }
        
        filename = f"shopping_session_{session_data['timestamp']}.json"
        self.engine.Cache.WriteCacheFile(filename, json.dumps(session_data, indent=2))
        self.engine.Log.WriteLog("shopping.log", f"Session saved: {total} {session_data['currency']}")
        
    def LoadShoppingSessions(self):
        """Load all shopping sessions"""
        sessions = []
        # Implementation to load all session files
        return sessions
        
    def GetCurrentTimestamp(self):
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
```

## 🚀 Mod Loading System

How the main app loads your mods:

```python
# In main app loader
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
        """Load individual mod"""
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

## 📚 Mod Examples

### 1. Terminal Mod
```python
# Simple terminal emulator
class TerminalMod(ModEngine):
    def RunCommand(self, command):
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
```

### 2. Task Manager Mod  
```python
# Task management
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

## 🛠️ Best Practices for Mods

1. **Own Language Packages**: Use the multi-language system
2. **State Management**: Use StateMachine for clean flow
3. **Persist Data**: Use Cache/Temp APIs for mod data
4. **Logging**: Log important mod events
5. **Error Handling**: Robust error handling implementation
6. **Configurable**: Load mod settings from JSON files
7. **Performance**: Use efficient data structures

## 🎉 Publishing Mods

1. **Testing**: Test thoroughly in different languages
2. **Documentation**: README with installation and usage
3. **Versioning**: Use semantic versioning
4. **Package.json**: Complete mod information
5. **Examples**: Code examples for other developers