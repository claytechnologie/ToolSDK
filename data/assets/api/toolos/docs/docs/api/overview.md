# API Overview

ToolOS SDK provides a comprehensive set of APIs for building desktop applications with internationalization support.

## Core APIs

### [Settings API](settings.md)
Manages application configuration with live reloading capabilities.

- ✅ Load/save JSON configuration files
- ✅ Dynamic settings updates
- ✅ Configuration validation
- ✅ Version management

### [Language API](language.md) 
Provides zero-configuration multi-language support.

- ✅ 7 built-in languages (de, en, es, fr, ru, sv, tr)
- ✅ 260+ pre-translated terms per language
- ✅ Custom language packages
- ✅ Dynamic language switching

### [Cache API](cache.md)
File-based caching system for temporary data storage.

- ✅ Write/read cache files
- ✅ Append content to existing files
- ✅ Cache existence checks
- ✅ Automatic cache directory creation

### [State Machine](statemachine.md)
Application flow control with predefined states.

- ✅ Predefined application states
- ✅ State transitions
- ✅ State validation
- ✅ Flow control logic

### [Temp API](temp.md)
Temporary file management system.

- ✅ Temporary file creation/deletion
- ✅ Automatic cleanup
- ✅ Content appending
- ✅ Existence validation

### [Log API](log.md)
Structured logging with timestamps.

- ✅ Timestamped log entries  
- ✅ Multiple log files
- ✅ Log file management
- ✅ Automatic log directory creation

### [Package API](package.md)
Package and mod management system.

- ✅ Simple authentication
- ✅ Package file operations
- ✅ Content management
- ✅ User session handling

## Usage Patterns

### Initialization

```python
from toolos.api import Api

# Initialize with settings file
app = Api("path/to/settings.json")
```

### Common Operations

```python
# Language translation
text = app.Language.Translate("welcome")

# State management
app.StateMachine.SetState(app.StateMachine.MAINMENU)
is_main_menu = app.StateMachine.IsState(app.StateMachine.MAINMENU)

# Caching
app.Cache.WriteCacheFile("data.json", json_data)
cached_data = app.Cache.ReadCacheFile("data.json")

# Logging
app.Log.WriteLog("app.log", "Event occurred")

# Settings
if app.Settings.CheckIfUpdate():
    app.Settings.Update()
```

## Error Handling

All APIs include proper error handling:

```python
try:
    data = app.Cache.ReadCacheFile("nonexistent.txt")
except FileNotFoundError:
    print("Cache file not found")

try:
    app.Settings.Update()
except json.JSONDecodeError:
    print("Invalid settings file format")
```

## Performance Considerations

- **Settings**: Updates are event-driven, no polling overhead
- **Language**: Translations are cached in memory after loading
- **Cache**: File-based operations, suitable for moderate data volumes
- **Logs**: Append-only operations for optimal performance

## Thread Safety

ToolOS SDK APIs are **not thread-safe** by design. For multi-threaded applications, implement proper synchronization around API calls.

## API Compatibility

ToolOS SDK follows semantic versioning. The current version is `1.3.2`:

- Major version changes may break API compatibility
- Minor version changes add features while maintaining compatibility  
- Patch versions contain only bug fixes