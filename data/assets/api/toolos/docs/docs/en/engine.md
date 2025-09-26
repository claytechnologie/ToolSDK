# Engine API

Complete documentation for the ToolOS Engine API with inheritance-based architecture.

## 🏗️ Base Class: engine.Api

The `engine.Api` class is the foundation of all ToolOS applications. When you inherit from this class, you get access to all framework APIs through simple inheritance.

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        # All APIs now available as self.Settings, self.Language, etc.
```

## 📋 Constructor Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `settings_file` | `str` | Yes | Path to your settings JSON file |

### Example Constructor Calls

```python
# Basic initialization
class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")

# With relative path
class MyApp(engine.Api):
    def __init__(self):
        super().__init__("config/app_settings.json")

# With absolute path
class MyApp(engine.Api):
    def __init__(self):
        super().__init__("/path/to/settings.json")
```

## 🎯 Available APIs After Inheritance

Once you inherit from `engine.Api`, these APIs are available:

### Core APIs
- **`self.Settings`** - Configuration management
- **`self.Language`** - Multi-language support
- **`self.Cache`** - Data caching system
- **`self.StateMachine`** - State management
- **`self.Temp`** - Temporary file handling
- **`self.Log`** - Logging system
- **`self.Package`** - Package/mod loading

## ⚙️ Settings API

Manage application configuration with ease.

### Methods

```python
# Get global settings
app_version = self.Settings.Global("app_version")
debug_mode = self.Settings.Global("debug_mode")

# Get user settings  
theme = self.Settings.User("theme")
language = self.Settings.User("language")

# Set settings
self.Settings.SetGlobal("app_version", "2.0.0")
self.Settings.SetUser("theme", "dark")

# Save changes
self.Settings.Save()
```

### Complete Example

```python
import toolos as engine

class ConfigApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Load application configuration
        self.LoadConfiguration()
        
    def LoadConfiguration(self):
        """Load and validate configuration"""
        # Get global settings
        self.AppVersion = self.Settings.Global("app_version")
        self.DebugMode = self.Settings.Global("debug_mode") == "true"
        
        # Get user preferences
        self.UserTheme = self.Settings.User("theme")
        self.AutoSave = self.Settings.User("auto_save") == "true"
        
        # Set defaults if not found
        if not self.AppVersion:
            self.Settings.SetGlobal("app_version", "1.0.0")
            self.AppVersion = "1.0.0"
            
        if not self.UserTheme:
            self.Settings.SetUser("theme", "dark")
            self.UserTheme = "dark"
            
        # Save any new defaults
        self.Settings.Save()
        
    def UpdateUserPreferences(self, theme, auto_save):
        """Update user preferences"""
        self.Settings.SetUser("theme", theme)
        self.Settings.SetUser("auto_save", "true" if auto_save else "false")
        self.Settings.Save()
        
        # Update local variables
        self.UserTheme = theme
        self.AutoSave = auto_save
```

## 🌍 Language API

Add multi-language support to your applications.

### Methods

```python
# Translate text
welcome_text = self.Language.Translate("welcome")
menu_title = self.Language.Translate("main_menu")

# Change language
self.Language.SetLanguage("de")  # German
self.Language.SetLanguage("en")  # English

# Get available languages
languages = self.Language.GetAvailableLanguages()

# Get current language
current = self.Language.GetCurrentLanguage()
```

### Multi-Language Application Example

```python
import toolos as engine

class MultiLangApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Initialize with user's preferred language
        preferred_lang = self.Settings.User("language")
        if preferred_lang:
            self.Language.SetLanguage(preferred_lang)
            
    def ShowLanguageMenu(self):
        """Display language selection menu"""
        print(f"\n=== {self.Language.Translate('language_selection')} ===")
        
        languages = self.Language.GetAvailableLanguages()
        current_lang = self.Language.GetCurrentLanguage()
        
        for i, lang in enumerate(languages):
            indicator = " ✓" if lang == current_lang else "  "
            print(f"{i + 1}.{indicator} {lang.upper()}")
        
        print()
        try:
            choice = int(input(self.Language.Translate("select_language"))) - 1
            if 0 <= choice < len(languages):
                new_lang = languages[choice]
                self.Language.SetLanguage(new_lang)
                
                # Save preference
                self.Settings.SetUser("language", new_lang)
                self.Settings.Save()
                
                print(self.Language.Translate("language_changed"))
            else:
                print(self.Language.Translate("invalid_selection"))
        except ValueError:
            print(self.Language.Translate("invalid_input"))
            
    def DisplayLocalizedMenu(self):
        """Show menu in current language"""
        print(f"\n{self.Language.Translate('welcome')}")
        print(f"=== {self.Language.Translate('main_menu')} ===")
        
        menu_items = [
            self.Language.Translate("start_game"),
            self.Language.Translate("settings"),
            self.Language.Translate("help"),
            self.Language.Translate("exit")
        ]
        
        for i, item in enumerate(menu_items):
            print(f"{i + 1}. {item}")
```

## 💾 Cache API  

Efficient data persistence and caching.

### Methods

```python
import json

# Write cache file
user_data = {"name": "John", "score": 1500}
self.Cache.WriteCacheFile("user.json", json.dumps(user_data))

# Read cache file
if self.Cache.CacheExists("user.json"):
    data = self.Cache.ReadCacheFile("user.json")
    user_data = json.loads(data)

# Delete cache file
self.Cache.DeleteCacheFile("old_data.json")

# List all cache files
cache_files = self.Cache.ListCacheFiles()
```

### Advanced Cache Example

```python
import toolos as engine
import json

class DataApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Load cached user data
        self.LoadUserData()
        
    def LoadUserData(self):
        """Load user data from cache"""
        if self.Cache.CacheExists("user_profile.json"):
            try:
                cached_data = self.Cache.ReadCacheFile("user_profile.json")
                self.UserProfile = json.loads(cached_data)
                self.Log.WriteLog("app.log", "User profile loaded from cache")
            except json.JSONDecodeError:
                self.Log.WriteLog("error.log", "Invalid JSON in user profile cache")
                self.CreateDefaultProfile()
        else:
            self.CreateDefaultProfile()
            
    def CreateDefaultProfile(self):
        """Create default user profile"""
        self.UserProfile = {
            "name": "Guest",
            "level": 1,
            "score": 0,
            "settings": {
                "difficulty": "normal",
                "sound": True,
                "notifications": True
            },
            "statistics": {
                "games_played": 0,
                "total_time": 0,
                "achievements": []
            }
        }
        self.SaveUserData()
        
    def SaveUserData(self):
        """Save user data to cache"""
        profile_data = json.dumps(self.UserProfile, indent=2)
        self.Cache.WriteCacheFile("user_profile.json", profile_data)
        self.Log.WriteLog("app.log", "User profile saved to cache")
        
    def UpdateUserStats(self, games_played=0, time_played=0):
        """Update user statistics"""
        stats = self.UserProfile["statistics"]
        stats["games_played"] += games_played
        stats["total_time"] += time_played
        
        self.SaveUserData()
        
    def AddAchievement(self, achievement_id, title, description):
        """Add achievement to user profile"""
        achievement = {
            "id": achievement_id,
            "title": title,
            "description": description,
            "earned_date": self.GetCurrentTimestamp()
        }
        
        self.UserProfile["statistics"]["achievements"].append(achievement)
        self.SaveUserData()
        
        self.Log.WriteLog("achievements.log", 
                         f"Achievement earned: {title}")
        
    def GetCurrentTimestamp(self):
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()
```

## 🔄 StateMachine API

Manage application states and flow.

### Methods

```python
# Set current state
self.StateMachine.SetState("main_menu")

# Get current state
current_state = self.StateMachine.GetState()

# Check if in specific state
if self.StateMachine.IsState("game_playing"):
    # Handle game state
    pass

# Get previous state
previous = self.StateMachine.PreviousState()
```

### State Machine Application

```python
import toolos as engine

class GameStates:
    MAIN_MENU = "main_menu"
    GAME_SETUP = "game_setup"
    PLAYING = "playing" 
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"
    EXIT = "exit"

class GameApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.States = GameStates()
        self.GameScore = 0
        self.GameLevel = 1
        
    def Run(self):
        """Main game loop with state management"""
        self.StateMachine.SetState(self.States.MAIN_MENU)
        
        while True:
            current_state = self.StateMachine.GetState()
            
            if self.StateMachine.IsState(self.States.MAIN_MENU):
                self.HandleMainMenu()
            elif self.StateMachine.IsState(self.States.GAME_SETUP):
                self.HandleGameSetup()
            elif self.StateMachine.IsState(self.States.PLAYING):
                self.HandleGamePlaying()
            elif self.StateMachine.IsState(self.States.PAUSED):
                self.HandleGamePaused()
            elif self.StateMachine.IsState(self.States.GAME_OVER):
                self.HandleGameOver()
            elif self.StateMachine.IsState(self.States.SETTINGS):
                self.HandleSettings()
            elif self.StateMachine.IsState(self.States.EXIT):
                break
                
    def HandleMainMenu(self):
        """Handle main menu state"""
        print(f"\n=== {self.Language.Translate('main_menu')} ===")
        print(f"1. {self.Language.Translate('new_game')}")
        print(f"2. {self.Language.Translate('settings')}")
        print(f"3. {self.Language.Translate('exit')}")
        
        choice = input(self.Language.Translate("input"))
        
        if choice == "1":
            self.StateMachine.SetState(self.States.GAME_SETUP)
        elif choice == "2":
            self.StateMachine.SetState(self.States.SETTINGS)
        elif choice == "3":
            self.StateMachine.SetState(self.States.EXIT)
            
    def HandleGamePlaying(self):
        """Handle game playing state"""
        print(f"\n{self.Language.Translate('game_playing')}")
        print(f"Score: {self.GameScore} | Level: {self.GameLevel}")
        print("P - Pause | Q - Quit")
        
        action = input().upper()
        
        if action == "P":
            self.StateMachine.SetState(self.States.PAUSED)
        elif action == "Q":
            self.StateMachine.SetState(self.States.GAME_OVER)
        else:
            # Simulate game logic
            self.GameScore += 10
            if self.GameScore % 100 == 0:
                self.GameLevel += 1
                
    def HandleGamePaused(self):
        """Handle game paused state"""
        print(f"\n{self.Language.Translate('game_paused')}")
        print("R - Resume | Q - Quit")
        
        action = input().upper()
        
        if action == "R":
            self.StateMachine.SetState(self.States.PLAYING)
        elif action == "Q":
            self.StateMachine.SetState(self.States.GAME_OVER)
```

## 📝 Logging API

Comprehensive logging system for debugging and monitoring.

### Methods

```python
# Create log file
self.Log.CreateLogFile("app.log")

# Write log entries
self.Log.WriteLog("app.log", "Application started")
self.Log.WriteLog("error.log", "Database connection failed")

# Read log file
logs = self.Log.ReadLog("app.log")
```

### Logging Best Practices

```python
import toolos as engine

class LoggingApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Initialize logging system
        self.InitializeLogging()
        
    def InitializeLogging(self):
        """Set up logging system"""
        # Create different log files for different purposes
        self.Log.CreateLogFile("app.log")      # General application logs
        self.Log.CreateLogFile("error.log")    # Error logs
        self.Log.CreateLogFile("user.log")     # User activity logs
        self.Log.CreateLogFile("debug.log")    # Debug information
        
        # Log application startup
        self.Log.WriteLog("app.log", "=== Application Started ===")
        self.Log.WriteLog("app.log", f"Version: {self.GetVersion()}")
        self.Log.WriteLog("app.log", f"Language: {self.Language.GetCurrentLanguage()}")
        
    def LogUserAction(self, action, details=""):
        """Log user actions"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] User Action: {action}"
        if details:
            log_entry += f" - {details}"
        
        self.Log.WriteLog("user.log", log_entry)
        
    def LogError(self, error_type, message, details=""):
        """Log errors with context"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        error_entry = f"[{timestamp}] ERROR: {error_type} - {message}"
        if details:
            error_entry += f"\nDetails: {details}"
            
        self.Log.WriteLog("error.log", error_entry)
        
    def LogDebug(self, component, message):
        """Log debug information"""
        debug_mode = self.Settings.Global("debug_mode") == "true"
        if debug_mode:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            debug_entry = f"[{timestamp}] DEBUG [{component}]: {message}"
            self.Log.WriteLog("debug.log", debug_entry)
            
    def GetVersion(self):
        """Get application version"""
        return self.Settings.Global("app_version") or "1.0.0"
        
    def HandleCriticalError(self, error):
        """Handle critical errors"""
        self.LogError("CRITICAL", str(error))
        
        # Also log to console for immediate attention
        print(f"CRITICAL ERROR: {error}")
        
        # Save application state before potential crash
        self.SaveEmergencyState()
        
    def SaveEmergencyState(self):
        """Save emergency state in case of critical error"""
        import json
        emergency_data = {
            "timestamp": self.GetCurrentTimestamp(),
            "state": self.StateMachine.GetState(),
            "settings": {
                "language": self.Language.GetCurrentLanguage(),
                "theme": self.Settings.User("theme")
            }
        }
        
        emergency_json = json.dumps(emergency_data, indent=2)
        self.Cache.WriteCacheFile("emergency_state.json", emergency_json)
        self.Log.WriteLog("app.log", "Emergency state saved")
```

## 🔧 Complete Application Example

Here's a complete example showing all APIs working together:

```python
import toolos as engine
import json

class AppStates:
    STARTUP = "startup"
    MAIN_MENU = "main_menu"
    USER_PROFILE = "user_profile"
    SETTINGS = "settings"
    EXIT = "exit"

class CompleteApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        
        # Application info
        self.AppName = "Complete ToolOS Example"
        self.Version = "1.0.0"
        self.States = AppStates()
        
        # Initialize systems
        self.InitializeSystems()
        
    def InitializeSystems(self):
        """Initialize all systems"""
        # Logging
        self.Log.CreateLogFile("app.log")
        self.Log.WriteLog("app.log", f"{self.AppName} v{self.Version} initializing")
        
        # Load user preferences
        self.LoadUserPreferences()
        
        # Load application data
        self.LoadApplicationData()
        
    def LoadUserPreferences(self):
        """Load user preferences from cache"""
        if self.Cache.CacheExists("user_prefs.json"):
            try:
                prefs_data = self.Cache.ReadCacheFile("user_prefs.json")
                self.UserPrefs = json.loads(prefs_data)
                
                # Apply language preference
                if "language" in self.UserPrefs:
                    self.Language.SetLanguage(self.UserPrefs["language"])
                    
            except json.JSONDecodeError:
                self.CreateDefaultPreferences()
        else:
            self.CreateDefaultPreferences()
            
    def CreateDefaultPreferences(self):
        """Create default user preferences"""
        self.UserPrefs = {
            "language": "en",
            "theme": "dark",
            "auto_save": True,
            "notifications": True
        }
        self.SaveUserPreferences()
        
    def SaveUserPreferences(self):
        """Save user preferences to cache"""
        prefs_data = json.dumps(self.UserPrefs, indent=2)
        self.Cache.WriteCacheFile("user_prefs.json", prefs_data)
        
    def LoadApplicationData(self):
        """Load application-specific data"""
        if self.Cache.CacheExists("app_data.json"):
            try:
                app_data = self.Cache.ReadCacheFile("app_data.json")
                self.AppData = json.loads(app_data)
            except json.JSONDecodeError:
                self.CreateDefaultAppData()
        else:
            self.CreateDefaultAppData()
            
    def CreateDefaultAppData(self):
        """Create default application data"""
        self.AppData = {
            "user_count": 0,
            "session_count": 0,
            "last_used": None,
            "features_used": []
        }
        self.SaveApplicationData()
        
    def SaveApplicationData(self):
        """Save application data to cache"""
        app_data = json.dumps(self.AppData, indent=2)
        self.Cache.WriteCacheFile("app_data.json", app_data)
        
    def Run(self):
        """Main application loop"""
        self.StateMachine.SetState(self.States.STARTUP)
        
        while True:
            if self.StateMachine.IsState(self.States.STARTUP):
                self.HandleStartup()
            elif self.StateMachine.IsState(self.States.MAIN_MENU):
                self.HandleMainMenu()
            elif self.StateMachine.IsState(self.States.USER_PROFILE):
                self.HandleUserProfile()
            elif self.StateMachine.IsState(self.States.SETTINGS):
                self.HandleSettings()
            elif self.StateMachine.IsState(self.States.EXIT):
                self.HandleExit()
                break
                
    def HandleStartup(self):
        """Handle application startup"""
        print(f"\n{self.Language.Translate('welcome')}")
        print(f"=== {self.AppName} v{self.Version} ===")
        
        # Update session count
        self.AppData["session_count"] += 1
        self.SaveApplicationData()
        
        # Log startup
        self.Log.WriteLog("app.log", "Application startup completed")
        
        # Move to main menu
        self.StateMachine.SetState(self.States.MAIN_MENU)
        
    def HandleMainMenu(self):
        """Handle main menu"""
        print(f"\n=== {self.Language.Translate('main_menu')} ===")
        
        menu_options = [
            self.Language.Translate("user_profile"),
            self.Language.Translate("settings"),
            self.Language.Translate("exit")
        ]
        
        for i, option in enumerate(menu_options):
            print(f"{i + 1}. {option}")
            
        choice = input(f"\n{self.Language.Translate('input')}")
        
        if choice == "1":
            self.StateMachine.SetState(self.States.USER_PROFILE)
        elif choice == "2":
            self.StateMachine.SetState(self.States.SETTINGS)
        elif choice == "3":
            self.StateMachine.SetState(self.States.EXIT)
        else:
            print(self.Language.Translate("invalid_choice"))
            
    def HandleExit(self):
        """Handle application exit"""
        self.Log.WriteLog("app.log", "Application shutting down")
        
        # Update last used timestamp
        import datetime
        self.AppData["last_used"] = datetime.datetime.now().isoformat()
        self.SaveApplicationData()
        
        # Clear temporary files
        self.Temp.ClearTemp()
        
        print(f"\n{self.Language.Translate('goodbye')}")

if __name__ == "__main__":
    app = CompleteApp()
    app.Run()
```

---

*This comprehensive Engine API guide shows you how to build professional applications with ToolOS inheritance-based architecture. Ready to create mods? Check out our [Modding SDK](modding-sdk.md)!* 🚀