# ToolOS

A lightweight Python app framework with mods, caching, settings and language API.

## Installation

```bash
pip install toolos
```

## Usage

```python
from toolos import Api

# Initialize the API
api = Api("settings.json")

# Use various components
api.Settings.LoadSettings()
api.Cache.WriteCacheFile("test.txt", "content")
api.Log.WriteLog("app.log", "Application started")
```

## Features

- Settings management
- Caching system
- Logging functionality
- Language localization
- State machine
- Package management
- Temporary file handling

## License

MIT