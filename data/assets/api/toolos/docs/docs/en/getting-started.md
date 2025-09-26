# Getting Started

Create your first ToolOS application in minutes with our inheritance-based architecture.

## 📋 Prerequisites

- Python 3.7 or higher
- Basic knowledge of Python classes and inheritance

## 🚀 Installation

### Step 1: Download ToolOS SDK

```bash
git clone https://github.com/claytechnologie/ToolSDK.git
cd ToolSDK
```

### Step 2: Project Structure

Create your project with this structure:

```
MyProject/
├── settings.json        # Application settings
├── app.py              # Your main application
└── data/
    └── lang/           # Language files
        ├── de.json     # German translations
        ├── en.json     # English translations
        └── ...
```

## 🏗️ Your First Application

### Step 1: Create settings.json

```json
{
    "global": {
        "language": "en",
        "app_version": "1.0.0",
        "debug_mode": false
    },
    "user": {
        "theme": "dark",
        "auto_save": true
    }
}
```

### Step 2: Create Language Files

**data/lang/en.json:**
```json
{
    "welcome": "Welcome to my application!",
    "main_menu": "Main Menu",
    "settings": "Settings",
    "exit": "Exit",
    "input": "Your choice: > "
}
```

**data/lang/de.json:**
```json
{
    "welcome": "Willkommen in meiner Anwendung!",
    "main_menu": "Hauptmenü",
    "settings": "Einstellungen", 
    "exit": "Beenden",
    "input": "Ihre Wahl: > "
}
```

### Step 3: Create Your Application

**app.py:**
```python
import toolos as engine

class AppStates:
    MAIN_MENU = "main_menu"
    SETTINGS = "settings" 
    EXIT = "exit"

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Application info
        self.AppName = "My First ToolOS App"
        self.Version = "1.0.0"
        self.States = AppStates()
        
        # Initialize logging
        self.Log.CreateLogFile("app.log")
        self.Log.WriteLog("app.log", f"{self.AppName} v{self.Version} started")
        
        # Load application configuration
        self.LoadAppConfig()
        
    def LoadAppConfig(self):
        """Load or create application configuration"""
        if not self.Cache.CacheExists("app_config.json"):
            import json
            default_config = {
                "theme": "dark",
                "notifications": True,
                "auto_save": True
            }
            
            config_data = json.dumps(default_config, indent=2)
            self.Cache.WriteCacheFile("app_config.json", config_data)
            self.AppConfig = default_config
        else:
            import json
            config_data = self.Cache.ReadCacheFile("app_config.json")
            self.AppConfig = json.loads(config_data)
    
    def Run(self):
        """Main application loop"""
        self.StateMachine.SetState(self.States.MAIN_MENU)
        
        while True:
            current_state = self.StateMachine.GetState()
            
            if self.StateMachine.IsState(self.States.MAIN_MENU):
                self.ShowMainMenu()
            elif self.StateMachine.IsState(self.States.SETTINGS):
                self.ShowSettings()
            elif self.StateMachine.IsState(self.States.EXIT):
                self.Cleanup()
                break
                
    def ShowMainMenu(self):
        """Display main menu"""
        print(f"\n{self.Language.Translate('welcome')}")
        print(f"=== {self.AppName} v{self.Version} ===\n")
        
        menu_options = [
            self.Language.Translate("settings"),
            self.Language.Translate("exit")
        ]
        
        for i, option in enumerate(menu_options):
            print(f"{i + 1}. {option}")
        
        print()
        choice = input(self.Language.Translate("input"))
        
        if choice == "1":
            self.StateMachine.SetState(self.States.SETTINGS)
        elif choice == "2":
            self.StateMachine.SetState(self.States.EXIT)
        else:
            print("Invalid choice!")
            
    def ShowSettings(self):
        """Display settings menu"""
        print(f"\n=== {self.Language.Translate('settings')} ===")
        print("1. Change Language")
        print("2. Toggle Theme")
        print("3. Back to Main Menu")
        
        choice = input(self.Language.Translate("input"))
        
        if choice == "1":
            self.ChangeLanguage()
        elif choice == "2":
            self.ToggleTheme()
        elif choice == "3":
            self.StateMachine.SetState(self.States.MAIN_MENU)
            
    def ChangeLanguage(self):
        """Change application language"""
        languages = self.Language.GetAvailableLanguages()
        
        print("\nAvailable languages:")
        for i, lang in enumerate(languages):
            current = " (current)" if lang == self.Language.GetCurrentLanguage() else ""
            print(f"{i + 1}. {lang}{current}")
        
        try:
            choice = int(input("Select language: ")) - 1
            if 0 <= choice < len(languages):
                selected_lang = languages[choice]
                self.Language.SetLanguage(selected_lang)
                self.Settings.SetGlobal("language", selected_lang)
                self.Settings.Save()
                
                self.Log.WriteLog("app.log", f"Language changed to: {selected_lang}")
                print(f"Language changed to: {selected_lang}")
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a number!")
            
    def ToggleTheme(self):
        """Toggle application theme"""
        current_theme = self.AppConfig.get("theme", "dark")
        new_theme = "light" if current_theme == "dark" else "dark"
        
        self.AppConfig["theme"] = new_theme
        
        import json
        config_data = json.dumps(self.AppConfig, indent=2)
        self.Cache.WriteCacheFile("app_config.json", config_data)
        
        self.Log.WriteLog("app.log", f"Theme changed to: {new_theme}")
        print(f"Theme changed to: {new_theme}")
        
    def Cleanup(self):
        """Clean up before exit"""
        self.Log.WriteLog("app.log", f"{self.AppName} shutting down")
        
        # Clear temporary files
        self.Temp.ClearTemp()
        
        print(f"\n{self.Language.Translate('exit')}...")
        print("Goodbye!")

if __name__ == "__main__":
    app = MyApp()
    app.Run()
```

### Step 4: Run Your Application

```bash
python app.py
```

## 🎯 Understanding the Code

### Inheritance Pattern

ToolOS uses clean inheritance instead of composition:

```python
# ✅ ToolOS way - Clean inheritance
class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        # All APIs available as self.Settings, self.Language, etc.
```

### Available APIs After Inheritance

Once you inherit from `engine.Api`, you have access to:

- `self.Settings` - Configuration management
- `self.Language` - Multi-language support  
- `self.Cache` - Data caching
- `self.StateMachine` - State management
- `self.Temp` - Temporary file handling
- `self.Log` - Logging system
- `self.Package` - Package/mod loading

### State Management

ToolOS applications use state machines for clean flow:

```python
class AppStates:
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    EXIT = "exit"

# In your app loop:
if self.StateMachine.IsState(self.States.MAIN_MENU):
    self.ShowMainMenu()
elif self.StateMachine.IsState(self.States.SETTINGS):
    self.ShowSettings()
```

### Language System

Add multi-language support easily:

```python
# Text translation
welcome = self.Language.Translate("welcome")

# Language switching
self.Language.SetLanguage("de")  # Switch to German
self.Language.SetLanguage("en")  # Switch to English
```

## 🚀 Advanced Features

### Custom Configuration Loading

```python
def LoadAdvancedConfig(self):
    """Load advanced configuration with validation"""
    config_file = "advanced_config.json"
    
    if self.Cache.CacheExists(config_file):
        import json
        try:
            config_data = self.Cache.ReadCacheFile(config_file)
            config = json.loads(config_data)
            
            # Validate configuration
            required_keys = ["database_url", "api_key", "max_connections"]
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Missing required config key: {key}")
                    
            self.AdvancedConfig = config
            self.Log.WriteLog("app.log", "Advanced configuration loaded successfully")
            
        except (json.JSONDecodeError, ValueError) as e:
            self.Log.WriteLog("error.log", f"Config error: {str(e)}")
            self.CreateDefaultAdvancedConfig()
    else:
        self.CreateDefaultAdvancedConfig()
        
def CreateDefaultAdvancedConfig(self):
    """Create default advanced configuration"""
    import json
    default_config = {
        "database_url": "sqlite:///app.db",
        "api_key": "your-api-key-here",
        "max_connections": 10,
        "timeout": 30,
        "retry_attempts": 3
    }
    
    config_data = json.dumps(default_config, indent=2)
    self.Cache.WriteCacheFile("advanced_config.json", config_data)
    self.AdvancedConfig = default_config
```

### Error Handling

```python
def SafeOperation(self):
    """Example of safe operations with error handling"""
    try:
        # Potentially risky operation
        data = self.Cache.ReadCacheFile("important_data.json")
        result = self.ProcessImportantData(data)
        
        # Log success
        self.Log.WriteLog("app.log", "Important operation completed successfully")
        return result
        
    except FileNotFoundError:
        self.Log.WriteLog("error.log", "Important data file not found")
        return self.CreateDefaultData()
        
    except json.JSONDecodeError:
        self.Log.WriteLog("error.log", "Invalid JSON in data file")
        return self.CreateDefaultData()
        
    except Exception as e:
        self.Log.WriteLog("error.log", f"Unexpected error: {str(e)}")
        return None
```

### Background Tasks

```python
def StartBackgroundTasks(self):
    """Start background tasks for your application"""
    import threading
    import time
    
    def AutoSaveTask():
        while self.StateMachine.GetState() != "exit":
            if self.AppConfig.get("auto_save", True):
                self.SaveApplicationState()
                self.Log.WriteLog("app.log", "Auto-save completed")
            time.sleep(300)  # Save every 5 minutes
    
    # Start background thread
    auto_save_thread = threading.Thread(target=AutoSaveTask, daemon=True)
    auto_save_thread.start()
```

## 📦 Next Steps

Now that you have your first ToolOS application running:

1. **[Engine API](engine.md)** - Learn about all available APIs
2. **[API Reference](api-reference.md)** - Complete method documentation
3. **[Modding SDK](modding-sdk.md)** - Create extensions and mods

## 🎯 Best Practices

1. **Always use inheritance** from `engine.Api`
2. **Initialize logging** early in your application
3. **Use state machines** for clean application flow
4. **Handle errors gracefully** with try-catch blocks
5. **Cache frequently used data** for better performance
6. **Support multiple languages** from the start
7. **Clean up resources** in your exit handler

## 🔧 Troubleshooting

### Common Issues

**Q: "Module not found" error**
A: Make sure ToolOS SDK is in your Python path or copy the toolos module to your project directory.

**Q: Language files not loading**
A: Check that your language files are in `data/lang/` directory and are valid JSON.

**Q: Settings not persisting**
A: Call `self.Settings.Save()` after making changes to settings.

**Q: Cache files not found**
A: Use `self.Cache.CacheExists()` before reading cache files.

---

*Ready to build more advanced features? Check out our [Engine API documentation](engine.md)!* 🚀