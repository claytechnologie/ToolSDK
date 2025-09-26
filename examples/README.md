# ToolOS SDK Examples 🚀

This directory contains practical examples showing how to use the ToolOS SDK.

## 📁 Examples

### 1. **Basic Multi-Language App** (`basic_multilang.py`)
Simple example showing language switching and translation.

### 2. **File Management Demo** (`file_management.py`) 
Demonstrates Cache, Temp, and Log APIs.

### 3. **Shopping Mod** (`shopping_example.py`)
Complete mod example with state management and custom language packages.

### 4. **Language Stress Test** (`language_test.py`)
Tests all 7 languages with comprehensive vocabulary.

## 🚀 Running Examples

```bash
# From the repository root
cd examples
python basic_multilang.py
python file_management.py
python shopping_example.py
```

## 📝 Creating Your Own

Use these examples as templates for your own projects:

1. **Copy an example** that matches your use case
2. **Modify the language packages** with your terms
3. **Add your business logic** to the existing structure
4. **Test with multiple languages** using `Settings.LANGUAGE = "de"`

## 🌍 Language Package Format

```json
{
    "welcome": "Welcome to my app!",
    "goodbye": "Thank you for using my app!",
    "error_message": "Something went wrong",
    "success_message": "Operation completed successfully"
}
```

## 💡 Tips

- **Override built-in terms**: Use the same key to override SDK vocabulary
- **Test all languages**: Switch `Settings.LANGUAGE` to test translations
- **Use meaningful keys**: `user_login_success` instead of `msg1`
- **Keep it simple**: Short, clear translation keys work best