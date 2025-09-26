# Examples

This page contains practical examples showing how to use ToolOS SDK in real-world scenarios.

## Complete Application Example

```python
import json
from toolos.api import Api

class TaskManager:
    def __init__(self):
        self.api = Api("settings.json")
        self.tasks = []
        self.load_tasks()
        
    def load_tasks(self):
        """Load tasks from cache"""
        if self.api.Cache.CacheExists("tasks.json"):
            data = self.api.Cache.ReadCacheFile("tasks.json")
            self.tasks = json.loads(data)
            self.api.Log.WriteLog("app.log", f"Loaded {len(self.tasks)} tasks")
    
    def save_tasks(self):
        """Save tasks to cache"""
        data = json.dumps(self.tasks, indent=2)
        self.api.Cache.WriteCacheFile("tasks.json", data)
        self.api.Log.WriteLog("app.log", "Tasks saved")
    
    def run(self):
        """Main application loop"""
        print(self.api.Language.Translate("welcome"))
        self.api.StateMachine.SetState(self.api.StateMachine.MAINMENU)
        
        while True:
            # Check for settings updates
            if self.api.Settings.CheckIfUpdate():
                self.api.Settings.Update()
                self.api.Language.Reload()
                print(self.api.Language.Translate("settings_updated"))
            
            # State machine logic
            if self.api.StateMachine.IsState(self.api.StateMachine.MAINMENU):
                choice = self.show_menu()
                self.handle_choice(choice)
            elif self.api.StateMachine.IsState(self.api.StateMachine.EXIT):
                break
                
        self.cleanup()
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*30)
        print(self.api.Language.Translate("task_manager"))
        print("="*30)
        
        options = [
            "add_task",
            "list_tasks", 
            "complete_task",
            "settings",
            "exit"
        ]
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {self.api.Language.Translate(option)}")
        
        try:
            choice = int(input(self.api.Language.Translate("input_prompt")))
            return choice
        except ValueError:
            print(self.api.Language.Translate("invalid_input"))
            return 0
    
    def handle_choice(self, choice):
        """Handle menu selection"""
        if choice == 1:
            self.add_task()
        elif choice == 2:
            self.list_tasks()
        elif choice == 3:
            self.complete_task()
        elif choice == 4:
            self.settings_menu()
        elif choice == 5:
            self.api.StateMachine.SetState(self.api.StateMachine.EXIT)
        else:
            print(self.api.Language.Translate("invalid_option"))
    
    def add_task(self):
        """Add new task"""
        title = input(self.api.Language.Translate("enter_task_title"))
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "completed": False,
            "created": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        print(self.api.Language.Translate("task_added"))
    
    def cleanup(self):
        """Cleanup before exit"""
        self.api.Temp.RemoveTempFile()  # Clean temp files
        self.api.Log.WriteLog("app.log", "Application closed")
        print(self.api.Language.Translate("goodbye"))

if __name__ == "__main__":
    app = TaskManager()
    app.run()
```

## Multi-Language Settings Manager

```python
from toolos.api import Api

class LanguageManager:
    def __init__(self):
        self.api = Api("settings.json")
        
    def show_language_menu(self):
        """Display available languages"""
        languages = self.api.Language.GetAvailableLanguages()
        
        print(self.api.Language.Translate("select_language"))
        for i, lang in enumerate(languages, 1):
            current = " *" if lang == self.api.Settings.LANGUAGE else ""
            print(f"{i}. {self.get_language_name(lang)}{current}")
    
    def get_language_name(self, code):
        """Get display name for language code"""
        names = {
            'de': 'Deutsch',
            'en': 'English', 
            'es': 'Español',
            'fr': 'Français',
            'ru': 'Русский',
            'sv': 'Svenska',
            'tr': 'Türkçe'
        }
        return names.get(code, code)
    
    def change_language(self, new_lang):
        """Change application language"""
        old_lang = self.api.Settings.LANGUAGE
        
        # Update settings
        self.api.Settings.LANGUAGE = new_lang
        self.api.Settings.SetUpdate()
        
        # Reload language
        self.api.Language.Reload()
        
        # Log change
        self.api.Log.WriteLog("language.log", 
            f"Language changed: {old_lang} -> {new_lang}")
        
        print(self.api.Language.Translate("language_changed"))
```

## Caching System Example

```python
import json
import time
from toolos.api import Api

class DataCache:
    def __init__(self):
        self.api = Api("settings.json")
        self.cache_timeout = 300  # 5 minutes
    
    def get_cached_data(self, cache_key):
        """Get data from cache with timeout check"""
        cache_file = f"{cache_key}.json"
        
        if not self.api.Cache.CacheExists(cache_file):
            return None
            
        try:
            data = self.api.Cache.ReadCacheFile(cache_file)
            cached = json.loads(data)
            
            # Check if cache is expired
            if time.time() - cached['timestamp'] > self.cache_timeout:
                self.api.Cache.RemoveCacheFile(cache_file)
                return None
                
            return cached['data']
        except (json.JSONDecodeError, KeyError):
            return None
    
    def set_cached_data(self, cache_key, data):
        """Store data in cache with timestamp"""
        cache_file = f"{cache_key}.json"
        cached = {
            'timestamp': time.time(),
            'data': data
        }
        
        self.api.Cache.WriteCacheFile(cache_file, json.dumps(cached))
        self.api.Log.WriteLog("cache.log", f"Cached data: {cache_key}")
    
    def expensive_operation(self, params):
        """Simulate expensive operation with caching"""
        cache_key = f"operation_{hash(str(params))}"
        
        # Try to get from cache first
        cached_result = self.get_cached_data(cache_key)
        if cached_result:
            self.api.Log.WriteLog("cache.log", f"Cache hit: {cache_key}")
            return cached_result
        
        # Perform expensive operation
        self.api.Log.WriteLog("cache.log", f"Cache miss: {cache_key}")
        result = self.simulate_work(params)
        
        # Cache the result
        self.set_cached_data(cache_key, result)
        return result
    
    def simulate_work(self, params):
        """Simulate time-consuming work"""
        time.sleep(2)  # Simulate processing time
        return f"Result for {params}"
```

## State Machine Workflow

```python
from toolos.api import Api

class WizardApp:
    def __init__(self):
        self.api = Api("settings.json")
        self.user_data = {}
    
    def run(self):
        """Run wizard with state machine"""
        while True:
            current_state = self.api.StateMachine.GetState()
            
            if self.api.StateMachine.IsState(self.api.StateMachine.FIRST_ENTRY):
                self.welcome_step()
                self.api.StateMachine.SetState(self.api.StateMachine.STEP_1)
                
            elif self.api.StateMachine.IsState(self.api.StateMachine.STEP_1):
                if self.personal_info_step():
                    self.api.StateMachine.SetState(self.api.StateMachine.STEP_2)
                    
            elif self.api.StateMachine.IsState(self.api.StateMachine.STEP_2):
                if self.preferences_step():
                    self.api.StateMachine.SetState(self.api.StateMachine.STEP_3)
                    
            elif self.api.StateMachine.IsState(self.api.StateMachine.STEP_3):
                self.confirmation_step()
                self.api.StateMachine.SetState(self.api.StateMachine.EXIT)
                
            elif self.api.StateMachine.IsState(self.api.StateMachine.EXIT):
                break
    
    def welcome_step(self):
        """Welcome screen"""
        print(self.api.Language.Translate("setup_wizard"))
        print(self.api.Language.Translate("welcome_message"))
        input(self.api.Language.Translate("press_enter"))
    
    def personal_info_step(self):
        """Collect personal information"""
        print(f"\n{self.api.Language.Translate('step')} 1: {self.api.Language.Translate('personal_info')}")
        
        name = input(self.api.Language.Translate("enter_name"))
        if not name:
            return False
            
        self.user_data['name'] = name
        self.api.Log.WriteLog("wizard.log", f"Name entered: {name}")
        return True
    
    def preferences_step(self):
        """Collect preferences"""
        print(f"\n{self.api.Language.Translate('step')} 2: {self.api.Language.Translate('preferences')}")
        
        # Language selection
        self.show_language_options()
        return True
    
    def confirmation_step(self):
        """Show confirmation and save"""
        print(f"\n{self.api.Language.Translate('step')} 3: {self.api.Language.Translate('confirmation')}")
        
        # Save user data
        self.api.Cache.WriteCacheFile("user_profile.json", 
                                     json.dumps(self.user_data, indent=2))
        
        print(self.api.Language.Translate("setup_complete"))
        self.api.Log.WriteLog("wizard.log", "Setup wizard completed")
```

## Error Handling Best Practices

```python
from toolos.api import Api
import json

class RobustApp:
    def __init__(self):
        try:
            self.api = Api("settings.json")
        except FileNotFoundError:
            print("Settings file not found, creating default...")
            self.create_default_settings()
            self.api = Api("settings.json")
        except json.JSONDecodeError:
            print("Invalid settings file format")
            raise
    
    def create_default_settings(self):
        """Create default settings file"""
        default_settings = {
            "version": "1.0.0",
            "language": "en",
            "mods_enabled": False,
            "cachepath": "data/cache",
            "temppath": "data/temp", 
            "logpath": "data/logs",
            "languagepath": "data/lang"
        }
        
        with open("settings.json", 'w') as f:
            json.dump(default_settings, f, indent=2)
    
    def safe_cache_operation(self, filename, data=None):
        """Safely perform cache operations"""
        try:
            if data:
                self.api.Cache.WriteCacheFile(filename, data)
                return True
            else:
                if self.api.Cache.CacheExists(filename):
                    return self.api.Cache.ReadCacheFile(filename)
                return None
        except (IOError, OSError) as e:
            self.api.Log.WriteLog("error.log", f"Cache error: {e}")
            return None
    
    def safe_translation(self, key, fallback=None):
        """Get translation with fallback"""
        try:
            translation = self.api.Language.Translate(key)
            return translation if translation != key else (fallback or key)
        except Exception as e:
            self.api.Log.WriteLog("error.log", f"Translation error: {e}")
            return fallback or key
```