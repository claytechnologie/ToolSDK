# ToolOS SDK

A lightweight Python app framework with inheritance-based architecture, multi-language support, and modular design.

## 📚 Documentation

**🌐 Complete Documentation:** https://claytechnologie.github.io/ToolSDK/

- 🇩🇪 **German**: https://claytechnologie.github.io/ToolSDK/
- 🇺🇸 **English**: https://claytechnologie.github.io/ToolSDK/en/

### Quick Links:
- 🚀 [Getting Started](https://claytechnologie.github.io/ToolSDK/getting-started/)
- 📋 [API Reference](https://claytechnologie.github.io/ToolSDK/api-reference/)
- 🎮 [Modding SDK](https://claytechnologie.github.io/ToolSDK/modding-sdk/)
- 🏗️ [Engine API](https://claytechnologie.github.io/ToolSDK/engine/)

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