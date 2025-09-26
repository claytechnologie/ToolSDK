# ToolOS SDK

Ein leichtgewichtiges, modulares Python Framework zum Entwickeln erweiterbarer Desktop-Anwendungen mit Zero-Configuration Internationalisierung.

*A lightweight, modular Python framework for building extensible desktop applications with zero-configuration internationalization.*

## 🚀 Features

- **🌍 Zero-Config Multi-Language** - 7 eingebaute Sprachen (de, en, es, fr, ru, sv, tr)
- **🧩 Vererbungsbasierte Architektur** - Einfaches Erben von Engine-Klassen
- **🔄 State Management** - Integrierte State Machine für App-Flow
- **💾 Caching & Temp Files** - Effiziente Dateiverwaltungs-APIs
- **⚙️ Live Settings** - Dynamische Konfiguration mit Live-Reload
- **📝 Logging System** - Strukturiertes Logging mit Timestamps
- **📦 Mod System** - Einfaches Mod/Plugin-System
- **🛠️ Helper Classes** - Utility-Klassen für häufige Aufgaben

## 🎯 Der ToolOS Weg - Vererbung

```python
import toolos as engine

class MyApp(engine.Api):
    def __init__(self):
        super().__init__("settings.json")
        self.isRunning = False
        
    def Run(self):
        print(self.Language.Translate("welcome"))
        self.StateMachine.SetState(self.StateMachine.MAINMENU)
        
        while self.isRunning:
            if self.StateMachine.IsState(self.StateMachine.MAINMENU):
                self.ShowMainMenu()
            elif self.StateMachine.IsState(self.StateMachine.EXIT):
                break
                
    def ShowMainMenu(self):
        print(self.Language.Translate("header"))
        choice = input(self.Language.Translate("input"))
        # Deine Menü-Logik hier...

# So einfach geht's!
app = MyApp()
app.Run()
```

## 🌍 Multi-Language by Default

ToolOS SDK comes with professional translations for 7 languages out of the box:

=== "German"
    ```python
    app.Language.Translate("welcome")  # "Willkommen im ToolOS!"
    ```

=== "English" 
    ```python
    app.Language.Translate("welcome")  # "Welcome to ToolOS!"
    ```

=== "French"
    ```python
    app.Language.Translate("welcome")  # "Bienvenue dans ToolOS!"
    ```

## 📦 Installation

```bash
pip install toolos
```

## 🏗️ Architektur

ToolOS SDK basiert auf Vererbung und modularen APIs:

| API | Beschreibung / Description |
|-----|----------------------------|
| **[Settings API](api/settings.md)** | 🔧 Konfigurationsmanagement mit Live-Reload / Configuration management with live reloading |
| **[Language API](api/language.md)** | 🌍 7-Sprachen-Support mit Custom Packages / 7-language support with custom packages |
| **[Cache API](api/cache.md)** | 💾 Datei-basierte Caching / File-based caching system |
| **[State Machine](api/statemachine.md)** | 🔄 App-Status-Management / Application state management |
| **[Temp API](api/temp.md)** | 🗂️ Temporäre Dateiverwaltung / Temporary file management |
| **[Log API](api/log.md)** | 📝 Strukturiertes Logging / Structured logging system |
| **[Package API](api/package.md)** | 📦 Mod-System / Package and mod management |
| **[Helper Classes](api/helpers.md)** | 🛠️ Utility-Klassen (Coming Soon) / Utility classes |

## 🎮 Modding SDK

Erstelle deine eigenen Mods und Erweiterungen:

- **[Modding Guide](modding-sdk.md)** - 🧩 Kompletter Guide zum Mod-Development
- **[Engine Vererbung](api/engine.md)** - 🏗️ Wie du deine eigene Engine erstellst
- **[Mod Examples](examples.md#mod-examples)** - 📚 Real-World Mod-Beispiele

## 🔧 Requirements

- Python 3.12+
- Windows/Linux/macOS

## 📖 Documentation

Explore the full documentation:

- [Getting Started Guide](getting-started.md)
- [API Reference](api/overview.md)
- [Examples](examples.md)
- [Contributing](contributing.md)

## 📄 License

MIT License - see the [LICENSE](https://github.com/claytechnologie/ToolSDK/blob/main/LICENSE) file for details.
