# Contributing

We welcome contributions to ToolOS SDK! This guide will help you get started with contributing to the project.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes** and test them
5. **Submit a pull request**

## 📋 Development Setup

### Prerequisites

- Python 3.12+
- Git
- Code editor (VS Code recommended)

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/ToolSDK.git
cd ToolSDK

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e .
pip install pytest black flake8 mypy
```

## 🎯 Areas for Contribution

### High Priority

- **New Language Support**: Add translations for additional languages
- **API Improvements**: Enhance existing APIs with new features
- **Documentation**: Improve code documentation and examples
- **Testing**: Add unit tests and integration tests

### Medium Priority

- **Performance**: Optimize file I/O operations
- **Error Handling**: Improve error messages and handling
- **Examples**: Create more real-world examples
- **Bug Fixes**: Address reported issues

### Low Priority

- **Code Style**: Improve code formatting and structure
- **Type Hints**: Add comprehensive type annotations
- **Refactoring**: Clean up legacy code

## 📝 Contribution Guidelines

### Code Style

We follow Python PEP 8 standards:

```bash
# Format code with black
black toolos/

# Check style with flake8
flake8 toolos/

# Type checking with mypy
mypy toolos/
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add Swedish language support
fix: resolve cache file encoding issue
docs: update API reference for LanguageAPI
test: add unit tests for StateMachineAPI
```

### Pull Request Process

1. **Create descriptive PR title**: Clearly state what the PR does
2. **Fill out PR template**: Provide context and testing details
3. **Link related issues**: Reference any related GitHub issues
4. **Request review**: Ask for review from maintainers
5. **Address feedback**: Respond to review comments promptly

## 🌍 Adding New Languages

To add support for a new language:

### 1. Create Language File

Create `data/assets/manager/lang/{language_code}.json`:

```json
{
  "welcome": "Welcome to ToolOS!",
  "settings": "Settings", 
  "exit": "Exit",
  "save": "Save",
  "cancel": "Cancel",
  // ... add all 260+ terms
}
```

### 2. Test Translation

```python
# Test your translation
from toolos.api import Api

api = Api("settings.json")
# Change language to your new language code
api.Settings.LANGUAGE = "your_lang_code"
api.Language.Reload()

# Test translations
print(api.Language.Translate("welcome"))
```

### 3. Update Documentation

- Add language to supported languages list
- Update examples with new language
- Add to README.md

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_language_api.py

# Run with coverage
pytest --cov=toolos
```

### Writing Tests

Create tests in the `tests/` directory:

```python
import pytest
from toolos.api import LanguageAPI, SettingsAPI

def test_language_translation():
    settings = SettingsAPI("test_settings.json")
    language = LanguageAPI(settings)
    
    # Test basic translation
    result = language.Translate("welcome")
    assert result != "welcome"  # Should be translated
    
    # Test fallback
    result = language.Translate("nonexistent_key")
    assert result == "nonexistent_key"
```

## 📚 Documentation

### Code Documentation

Use clear docstrings for all public methods:

```python
def Translate(self, key: str) -> str:
    """
    Translates a key to the current language.
    
    Args:
        key: The translation key to look up
        
    Returns:
        The translated text, or the key itself if not found
        
    Example:
        >>> lang.Translate("welcome")
        "Welcome to ToolOS!"
    """
    return self.language_data.get(key, key)
```

### API Documentation

Update relevant documentation files:

- API reference pages in `docs/docs/api/`
- Examples in `docs/docs/examples.md`
- Getting started guide

## 🐛 Bug Reports

When reporting bugs, include:

1. **Python version** and operating system
2. **ToolOS SDK version**
3. **Minimal code example** that reproduces the issue
4. **Expected vs actual behavior**
5. **Full error traceback** if applicable

Use this template:

```markdown
## Bug Description
Brief description of the issue

## Environment
- Python version: 3.12.0
- ToolOS SDK version: 1.3.2
- OS: Windows 11 / Ubuntu 22.04 / macOS 14

## Steps to Reproduce
1. Step one
2. Step two
3. Issue occurs

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Code Example
```python
# Minimal code that reproduces the issue
```
```

## 💡 Feature Requests

Before submitting feature requests:

1. **Check existing issues** to avoid duplicates
2. **Provide clear use case** explaining why the feature is needed
3. **Consider implementation** and suggest possible approaches
4. **Think about backwards compatibility**

## 📄 License

By contributing to ToolOS SDK, you agree that your contributions will be licensed under the same MIT License that covers the project.

## 🤝 Community

- **GitHub Discussions**: For questions and general discussion
- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions

## 📞 Getting Help

Need help with contributing?

- Check the [documentation](https://claytechnologie.github.io/ToolSDK-docs/)
- Look at existing issues and PRs for examples
- Ask questions in GitHub Discussions
- Contact maintainers through GitHub

Thank you for contributing to ToolOS SDK! 🎉