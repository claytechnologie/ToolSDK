# API Reference

Complete API reference for all ToolOS SDK components.

## 🏗️ Engine.Api (Base Class)

| Component | Type | Description | Available Methods |
|------------|------|-------------|-------------------|
| `self.Settings` | ToolOS.Settings | Configuration management | `Global()`, `User()`, `Save()`, `LoadSettings()` |
| `self.Language` | ToolOS.Language | Multi-language system | `Translate()`, `SetLanguage()`, `AddLanguagePackage()` |
| `self.Cache` | ToolOS.Cache | Cache management | `WriteCacheFile()`, `ReadCacheFile()`, `CacheExists()` |
| `self.StateMachine` | ToolOS.StateMachine | State management | `SetState()`, `GetState()`, `IsState()` |
| `self.Temp` | ToolOS.Temp | Temporary files | `WriteTempFile()`, `ReadTempFile()`, `TempExists()` |
| `self.Log` | ToolOS.Log | Logging system | `WriteLog()`, `ReadLog()`, `CreateLogFile()` |
| `self.Package` | ToolOS.Package | Package management | `LoadPackage()`, `GetPackageInfo()`, `ListPackages()` |

## ⚙️ Settings API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `Global(key)` | `key: str` | `str` | Get global setting |
| `User(key)` | `key: str` | `str` | Get user setting |
| `Save()` | - | `bool` | Save settings |
| `LoadSettings()` | - | `dict` | Load all settings |
| `SetGlobal(key, value)` | `key: str, value: str` | `bool` | Set global setting |
| `SetUser(key, value)` | `key: str, value: str` | `bool` | Set user setting |

### Settings Examples

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Get settings
        language = self.Settings.Global("language")
        user_theme = self.Settings.User("theme")
        
        # Set settings
        self.Settings.SetGlobal("app_version", "1.0.0")
        self.Settings.SetUser("last_login", "2024-01-01")
        self.Settings.Save()
```

## 🌍 Language API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `Translate(key)` | `key: str` | `str` | Translate text |
| `SetLanguage(lang)` | `lang: str` | `bool` | Change language |
| `AddLanguagePackage(lang, file_path)` | `lang: str, file_path: str` | `bool` | Add language package |
| `GetAvailableLanguages()` | - | `list` | Available languages |
| `GetCurrentLanguage()` | - | `str` | Current language |
| `Reload()` | - | `bool` | Reload language packages |

### Language Examples

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Translate text
        welcome_text = self.Language.Translate("welcome")
        menu_title = self.Language.Translate("main_menu")
        
        # Change language
        self.Language.SetLanguage("en")
        
        # Show available languages
        languages = self.Language.GetAvailableLanguages()
        print(f"Available languages: {languages}")
```

## 💾 Cache API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `WriteCacheFile(filename, data)` | `filename: str, data: str` | `bool` | Write cache file |
| `ReadCacheFile(filename)` | `filename: str` | `str` | Read cache file |
| `CacheExists(filename)` | `filename: str` | `bool` | Cache file exists |
| `DeleteCacheFile(filename)` | `filename: str` | `bool` | Delete cache file |
| `ListCacheFiles()` | - | `list` | All cache files |
| `ClearCache()` | - | `bool` | Clear entire cache |

### Cache Examples

```python
import toolos as engine
import json

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Cache data
        user_data = {"name": "John", "score": 1500}
        self.Cache.WriteCacheFile("user_data.json", json.dumps(user_data))
        
        # Load data from cache
        if self.Cache.CacheExists("user_data.json"):
            cached_data = self.Cache.ReadCacheFile("user_data.json")
            user_data = json.loads(cached_data)
            print(f"Username: {user_data['name']}")
```

## 🔄 StateMachine API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `SetState(state)` | `state: str` | `bool` | Set state |
| `GetState()` | - | `str` | Get current state |
| `IsState(state)` | `state: str` | `bool` | Check state |
| `PreviousState()` | - | `str` | Get previous state |
| `StateHistory()` | - | `list` | State history |
| `ResetState()` | - | `bool` | Reset state |

### StateMachine Examples

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

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `WriteTempFile(filename, data)` | `filename: str, data: str` | `bool` | Write temp file |
| `ReadTempFile(filename)` | `filename: str` | `str` | Read temp file |
| `TempExists(filename)` | `filename: str` | `bool` | Temp file exists |
| `DeleteTempFile(filename)` | `filename: str` | `bool` | Delete temp file |
| `ListTempFiles()` | - | `list` | All temp files |
| `ClearTemp()` | - | `bool` | Clear temp folder |

### Temp Examples

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Create temporary file
        temp_data = "Temporary processing data"
        self.Temp.WriteTempFile("processing.txt", temp_data)
        
        # Process temporary file
        if self.Temp.TempExists("processing.txt"):
            data = self.Temp.ReadTempFile("processing.txt")
            # Processing...
            self.Temp.DeleteTempFile("processing.txt")
```

## 📝 Log API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `WriteLog(filename, message)` | `filename: str, message: str` | `bool` | Write log entry |
| `ReadLog(filename)` | `filename: str` | `str` | Read log file |
| `CreateLogFile(filename)` | `filename: str` | `bool` | Create log file |
| `LogExists(filename)` | `filename: str` | `bool` | Log file exists |
| `ClearLog(filename)` | `filename: str` | `bool` | Clear log file |
| `ListLogFiles()` | - | `list` | All log files |

### Log Examples

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Initialize logging
        self.Log.CreateLogFile("app.log")
        
        # Write log entries
        self.Log.WriteLog("app.log", "Application started")
        self.Log.WriteLog("app.log", "User logged in")
        self.Log.WriteLog("error.log", "Database connection failed")
        
        # Read logs
        app_logs = self.Log.ReadLog("app.log")
        print("App Logs:", app_logs)
```

## 📦 Package API

| Method | Parameters | Returns | Description |
|---------|------------|---------|-------------|
| `LoadPackage(package_name)` | `package_name: str` | `object` | Load package |
| `GetPackageInfo(package_name)` | `package_name: str` | `dict` | Package information |
| `ListPackages()` | - | `list` | All packages |
| `PackageExists(package_name)` | `package_name: str` | `bool` | Package exists |
| `ReloadPackage(package_name)` | `package_name: str` | `bool` | Reload package |
| `UnloadPackage(package_name)` | `package_name: str` | `bool` | Unload package |

### Package Examples

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Load package
        shopping_mod = self.Package.LoadPackage("Shopping")
        task_manager = self.Package.LoadPackage("TaskManager")
        
        # Get package information
        package_info = self.Package.GetPackageInfo("Shopping")
        print(f"Package: {package_info['name']} v{package_info['version']}")
        
        # List all available packages
        packages = self.Package.ListPackages()
        for package in packages:
            print(f"- {package}")
```

## 🚀 Complete App Example

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # App-specific initialization
        self.AppName = "My ToolOS App"
        self.Version = "1.0.0"
        
        # Initialize logging
        self.Log.CreateLogFile("app.log")
        self.Log.WriteLog("app.log", f"{self.AppName} v{self.Version} started")
        
        # Load default configuration
        self.InitializeConfig()
        
    def InitializeConfig(self):
        """Initialize app configuration"""
        if not self.Cache.CacheExists("app_config.json"):
            import json
            default_config = {
                "theme": "dark",
                "auto_save": True,
                "notifications": True
            }
            self.Cache.WriteCacheFile("app_config.json", json.dumps(default_config))
            
    def Run(self):
        """Main app loop"""
        while True:
            if self.StateMachine.IsState("main_menu"):
                self.ShowMainMenu()
            elif self.StateMachine.IsState("exit"):
                self.Cleanup()
                break
                
    def ShowMainMenu(self):
        """Show main menu"""
        print(self.Language.Translate("welcome"))
        # Menu logic...
        
    def Cleanup(self):
        """Clean up before exit"""
        self.Log.WriteLog("app.log", f"{self.AppName} shutting down")
        self.Temp.ClearTemp()  # Clear temporary files
        
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
            # Critical operation
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
        # Data processing
        pass
```

## 📊 Performance Tips

1. **Use Caching**: Cache frequently used data
2. **Optimize Logging**: Don't log too verbosely
3. **Temp Files**: Store large data temporarily
4. **State Management**: Clean state transitions
5. **Language Loading**: Load languages only when needed
6. **Package Loading**: Load packages lazily