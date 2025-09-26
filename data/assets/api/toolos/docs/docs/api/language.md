# Language API

The Language API provides zero-configuration internationalization with 7 built-in languages and 260+ pre-translated terms.

## Class Reference

::: toolos.api.LanguageAPI

## Supported Languages

ToolOS SDK includes professional translations for:

| Code | Language | Terms | Status |
|------|----------|-------|--------|
| `de` | German | 260+ | ✅ Complete |
| `en` | English | 260+ | ✅ Complete |  
| `es` | Spanish | 260+ | ✅ Complete |
| `fr` | French | 260+ | ✅ Complete |
| `ru` | Russian | 260+ | ✅ Complete |
| `sv` | Swedish | 260+ | ✅ Complete |
| `tr` | Turkish | 260+ | ✅ Complete |

## Basic Usage

### Initialization

```python
from toolos.api import LanguageAPI, SettingsAPI

# Initialize with settings (automatically detects language)
settings = SettingsAPI("settings.json")
language = LanguageAPI(settings)
```

### Translation

```python
# Translate text using current language
welcome = language.Translate("welcome")  # "Welcome to ToolOS!" (en)
settings = language.Translate("settings")  # "Settings" (en)
exit_app = language.Translate("exit")  # "Exit" (en)

# If translation not found, returns the key itself
unknown = language.Translate("unknown_key")  # "unknown_key"
```

## Common Translations

Here are some frequently used translations across all languages:

### UI Elements
```python
language.Translate("welcome")      # Welcome message
language.Translate("settings")     # Settings menu
language.Translate("exit")         # Exit/Quit
language.Translate("back")         # Back button
language.Translate("next")         # Next button
language.Translate("save")         # Save action
language.Translate("cancel")       # Cancel action
```

### System Messages
```python
language.Translate("app_is_running")    # App running status
language.Translate("invalid_option")   # Invalid input message
language.Translate("settings_saved")   # Settings saved confirmation
language.Translate("exiting_app")      # App exit message
```

### Error Messages
```python
language.Translate("error")            # Generic error
language.Translate("warning")          # Warning message
language.Translate("file_not_found")   # File not found error
language.Translate("permission_denied") # Access denied error
```

## Language Management

### Available Languages

```python
# Get list of available language codes
languages = language.GetAvailableLanguages()
print(languages)  # ['de', 'en', 'es', 'fr', 'ru', 'sv', 'tr']
```

### Dynamic Language Switching

```python
# Change language in settings
settings.LANGUAGE = "de"
settings.SetUpdate()

# Reload language data
language.Reload()

# Now translations are in German
welcome = language.Translate("welcome")  # "Willkommen im ToolOS!"
```

### Get All Translation Keys

```python
# Get all available translation keys
keys = language.GetAllTranslationKeys()
print(f"Available translations: {len(keys)}")
```

## Custom Language Packages

Extend translations with custom language packages:

### Adding Custom Translations

```python
# Create custom translation file: my_translations.json
{
  "custom_greeting": "Hello from my app!",
  "custom_error": "Something went wrong in my feature"
}

# Add to language system
language.AddLanguagePackage("en", "my_translations.json")

# Use custom translations
greeting = language.Translate("custom_greeting")
```

### Language Package Format

Custom language files should follow this JSON structure:

```json
{
  "key1": "Translation 1",
  "key2": "Translation 2", 
  "nested_key": "Nested translation",
  "app_specific_term": "Your app's specific translation"
}
```

## Advanced Features

### Fallback Mechanism

If a translation is not found:
1. Returns the original key as fallback
2. Allows graceful degradation 
3. Makes missing translations obvious for debugging

```python
# Missing translation returns key itself
missing = language.Translate("nonexistent_key")
print(missing)  # "nonexistent_key"
```

### Reload After Settings Change

```python
# Complete reload workflow
if settings.CheckIfUpdate():
    settings.Update()
    language.Reload()  # Critical: reload language after settings change
    
    # Now using new language
    message = language.Translate("settings_changed")
```

## Methods Reference

### `Translate(key)`
Translates a key to the current language.

**Parameters:**
- `key` (str): Translation key to look up

**Returns:** `str` - Translated text or the key itself if not found

### `Reload()`
Reloads language data after settings change. Call this whenever the language setting changes.

### `GetAllTranslationKeys()`
Returns all available translation keys in the current language.

**Returns:** `list[str]` - List of all translation keys

### `GetAvailableLanguages()`
Returns list of available language codes.

**Returns:** `list[str]` - List of language codes (e.g., ['de', 'en', 'fr'])

### `AddLanguagePackage(language, datapath)`
Adds custom translation package for a specific language.

**Parameters:**
- `language` (str): Language code (e.g., 'en', 'de') 
- `datapath` (str): Path to JSON file containing translations

## Language Files Location

Language files are stored in the path specified by `settings.LANGUAGEPATH`:

```
data/assets/manager/lang/
├── de.json    # German translations
├── en.json    # English translations  
├── es.json    # Spanish translations
├── fr.json    # French translations
├── ru.json    # Russian translations
├── sv.json    # Swedish translations
└── tr.json    # Turkish translations
```

## Best Practices

1. **Always call Reload()**: After changing language settings, always call `language.Reload()`
2. **Use descriptive keys**: Choose clear, consistent translation keys
3. **Fallback handling**: Design UI to handle missing translations gracefully
4. **Test all languages**: Verify your app works with all supported languages
5. **Custom packages**: Use custom language packages for app-specific terms

## Example: Multi-Language Menu

```python
class MultiLanguageMenu:
    def __init__(self, settings, language):
        self.settings = settings
        self.language = language
        
    def show_menu(self):
        """Display menu in current language"""
        print("=" * 30)
        print(self.language.Translate("header"))
        print("=" * 30)
        print()
        
        options = [
            ("settings", "settings"),
            ("help", "help"), 
            ("about", "about"),
            ("exit", "exit")
        ]
        
        for i, (key, _) in enumerate(options):
            text = self.language.Translate(key)
            print(f"{i + 1}. {text}")
    
    def change_language(self, new_lang):
        """Change language and reload menu"""
        self.settings.LANGUAGE = new_lang
        self.settings.SetUpdate()
        self.language.Reload()
        print(self.language.Translate("language_changed"))

# Usage
menu = MultiLanguageMenu(settings, language)
menu.show_menu()  # Shows menu in current language
menu.change_language("de")  # Switch to German
menu.show_menu()  # Shows menu in German
```