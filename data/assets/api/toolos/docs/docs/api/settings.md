# Settings API

The Settings API manages application configuration with support for dynamic updates and live reloading.

## Class Reference

::: toolos.api.SettingsAPI

## Key Features

- **JSON Configuration**: Load settings from JSON files with UTF-8 encoding
- **Live Reloading**: Detect and apply configuration changes at runtime
- **Property Access**: Easy access to common settings through properties
- **Update Mechanism**: Built-in update flag system for change detection

## Basic Usage

### Initialization

```python
from toolos.api import SettingsAPI

# Initialize with settings file path
settings = SettingsAPI("path/to/settings.json")
```

### Accessing Settings

```python
# Access common properties
version = settings.VERSION
language = settings.LANGUAGE
cache_path = settings.CACHEPATH

# Access any setting by key
custom_value = settings.Global("custom_setting")
```

### Settings File Format

Your `settings.json` should follow this structure:

```json
{
  "version": "1.0.0",
  "language": "en",
  "mods_enabled": true,
  "cachepath": "data/cache",
  "temppath": "data/temp",
  "logpath": "data/logs",
  "languagepath": "data/lang",
  "packagepath": "data/packages",
  "apipath": "data/api",
  "modpath": "data/mods",
  "update": false
}
```

## Dynamic Updates

### Check for Updates

```python
# Check if settings were modified
if settings.CheckIfUpdate():
    print("Settings have been updated")
```

### Trigger Updates

```python
# Mark settings for update (sets update flag to True)
settings.SetUpdate()

# Reload settings from file
settings.Update()
```

### Update Workflow

```python
# Typical update workflow
if settings.CheckIfUpdate():
    # Reload settings from disk
    settings.Update()
    
    # Reload dependent systems
    language.Reload()  # If language changed
    
    print("Settings updated successfully")
```

## Available Properties

| Property | Description | Default |
|----------|-------------|---------|
| `VERSION` | Application version | `None` |
| `LANGUAGE` | Current language code | `None` |
| `PACKAGEPATH` | Package directory path | `None` |
| `CACHEPATH` | Cache directory path | `None` |
| `TEMPPATH` | Temporary files path | `None` |
| `LOGPATH` | Log files directory | `None` |
| `APIPATH` | API files directory | `None` |
| `LANGUAGEPATH` | Language files directory | `None` |
| `MODPATH` | Mods directory path | `None` |
| `MODS_ENABLED` | Whether mods are enabled | `False` |

## Methods

### `LoadSettings()`
Loads settings from the JSON file specified in `SETTINGSPATH`.

**Returns:** `dict` - The loaded settings dictionary

**Raises:** `FileNotFoundError`, `json.JSONDecodeError`

### `Global(key)`
Retrieves a setting value by key.

**Parameters:**
- `key` (str): The setting key to retrieve

**Returns:** `Any` - The setting value or `None` if not found

### `SetUpdate()`
Sets the update flag to `True` in the settings file, indicating that settings have been modified.

### `CheckIfUpdate()`
Checks if the update flag is set in the current settings.

**Returns:** `bool` - `True` if update flag is set

### `Update()`
Reloads all settings from the file and updates all properties.

## Error Handling

```python
try:
    settings = SettingsAPI("settings.json")
except FileNotFoundError:
    print("Settings file not found")
except json.JSONDecodeError:
    print("Invalid JSON format")

try:
    settings.Update()
except Exception as e:
    print(f"Failed to update settings: {e}")
```

## Best Practices

1. **Use absolute paths**: Provide full paths to avoid path resolution issues
2. **Handle missing files**: Always wrap initialization in try-catch blocks
3. **Regular updates**: Check for updates in your main application loop
4. **Backup settings**: Keep backup copies of configuration files
5. **Validate settings**: Verify required keys exist after loading

## Example: Complete Settings Management

```python
import json
from toolos.api import SettingsAPI

class AppSettings:
    def __init__(self, settings_path):
        self.settings = SettingsAPI(settings_path)
        self.callbacks = []
    
    def add_update_callback(self, callback):
        """Add callback to be called when settings update"""
        self.callbacks.append(callback)
    
    def check_and_update(self):
        """Check for updates and notify callbacks"""
        if self.settings.CheckIfUpdate():
            self.settings.Update()
            
            # Notify all callbacks
            for callback in self.callbacks:
                callback(self.settings)
            
            return True
        return False
    
    def get_safe(self, key, default=None):
        """Safely get setting with default value"""
        return self.settings.Global(key) or default

# Usage
app_settings = AppSettings("config.json")
app_settings.add_update_callback(lambda s: print(f"Language changed to: {s.LANGUAGE}"))

# In main loop
if app_settings.check_and_update():
    print("Settings were updated")
```