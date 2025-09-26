# ToolOS SDK Documentation

Welcome to ToolOS SDK - A lightweight Python application framework with inheritance-based architecture, multilingual support, and modular design.

## 🚀 What is ToolOS SDK?

ToolOS SDK is a professional framework for building Python applications with:

- **Inheritance Architecture**: Simple class inheritance from `engine.Api`
- **Multilingual Support**: 7 languages with dynamic switching
- **State Management**: Clean state-based application flow
- **Caching System**: Efficient data caching and persistence
- **Logging**: Comprehensive logging with multiple log files
- **Modular Design**: Plugin/mod system for extensibility

## 💡 Quick Start

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.AppName = "My Application"
        
    def Run(self):
        welcome_text = self.Language.Translate("welcome")
        print(f"{welcome_text} - {self.AppName}")
        
        # Your application logic here
        self.StateMachine.SetState("main_menu")
        
if __name__ == "__main__":
    app = MyApp()
    app.Run()
```

## 🛠️ Core Features

### 🏗️ Inheritance-Based Architecture
Instead of composition, ToolOS uses clean inheritance:

```python
# ✅ ToolOS Way - Clean inheritance
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        # All APIs available via self.Settings, self.Language, etc.
```

### 🌍 Multi-Language Support
Built-in support for 7 languages with easy switching:

```python
# Language switching
self.Language.SetLanguage("en")  # English
self.Language.SetLanguage("de")  # German
self.Language.SetLanguage("fr")  # French

# Text translation
welcome = self.Language.Translate("welcome")
menu_title = self.Language.Translate("main_menu")
```

### 💾 Smart Caching System
Efficient data persistence with simple API:

```python
# Save data to cache
import json
user_data = {"name": "John", "score": 1500}
self.Cache.WriteCacheFile("user.json", json.dumps(user_data))

# Load data from cache
if self.Cache.CacheExists("user.json"):
    data = self.Cache.ReadCacheFile("user.json")
    user_data = json.loads(data)
```

### 🔄 State Management
Clean state-based application flow:

```python
class AppStates:
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    EXIT = "exit"

class MyApp(engine.Api):
    def Run(self):
        while True:
            if self.StateMachine.IsState(AppStates.MAIN_MENU):
                self.ShowMainMenu()
            elif self.StateMachine.IsState(AppStates.EXIT):
                break
```

## 📦 Available APIs

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| **Settings** | Configuration management | `Global()`, `User()`, `Save()` |
| **Language** | Multi-language support | `Translate()`, `SetLanguage()` |
| **Cache** | Data caching | `WriteCacheFile()`, `ReadCacheFile()` |
| **StateMachine** | State management | `SetState()`, `IsState()` |
| **Temp** | Temporary files | `WriteTempFile()`, `ReadTempFile()` |
| **Log** | Logging system | `WriteLog()`, `ReadLog()` |
| **Package** | Mod/package loading | `LoadPackage()`, `ListPackages()` |

## 🎮 Real-World Example

Here's how the Shopping mod from your codebase uses ToolOS:

```python
import toolos as engine

class ShoppingApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.AppName = "Shopping Simulator"
        self.Version = "2.0.4"
        
        # Initialize logging
        self.Log.CreateLogFile("shopping.log")
        self.Log.WriteLog("shopping.log", f"{self.AppName} v{self.Version} started")
        
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
        # Shopping logic with state management
        self.StateMachine.SetState("shopping_mode")
        # Save shopping session to cache
        session_data = {"items": [], "total": 0.0}
        self.Cache.WriteCacheFile("current_session.json", 
                                json.dumps(session_data))
```

## 🌟 Why Choose ToolOS?

- **Simple**: One base class, clean inheritance
- **Powerful**: Full-featured APIs for all common tasks
- **Multilingual**: Built-in support for international applications
- **Extensible**: Mod system for custom functionality
- **Professional**: Used in production applications
- **CamelCase**: Human-readable method names
- **Well-documented**: Comprehensive documentation and examples

## 📚 Next Steps

1. **[Getting Started](getting-started.md)** - Create your first ToolOS application
2. **[Engine API](engine.md)** - Learn the core inheritance API
3. **[API Reference](api-reference.md)** - Complete API documentation
4. **[Modding SDK](modding-sdk.md)** - Build mods and extensions

## 🤝 Community & Support

ToolOS SDK is actively developed and maintained. Join our community:

- **GitHub**: [ToolOS SDK Repository](https://github.com/claytechnologie/ToolSDK)
- **Documentation**: This site with full examples
- **Issues**: Report bugs and request features
- **Examples**: Real-world applications in the repository

---

*Ready to build professional Python applications? Let's get started!* 🚀