"""
ToolOS SDK - Basic Multi-Language Example
==========================================

This example demonstrates:
- Basic SDK initialization
- Language switching
- Custom language packages
- Built-in vocabulary usage
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.assets.api.tool_api import ToolAPI

class BasicMultiLangApp(ToolAPI):
    
    def __init__(self):
        super().__init__(name="BasicApp", version="1.0.0")
        
        # Add custom language packages
        self.add_custom_languages()
        
    def add_custom_languages(self):
        """Add custom language packages for our app"""
        
        # Create custom English terms
        english_custom = {
            "app_welcome": "Welcome to Basic Multi-Language App!",
            "language_demo": "Language demonstration:",
            "custom_message": "This is a custom message!",
            "goodbye_message": "Thank you for trying our app!"
        }
        
        # Create custom German terms  
        german_custom = {
            "app_welcome": "Willkommen zur Basis Mehrsprachigen App!",
            "language_demo": "Sprach-Demonstration:",
            "custom_message": "Das ist eine benutzerdefinierte Nachricht!",
            "goodbye_message": "Danke, dass Sie unsere App ausprobiert haben!"
        }
        
        # Write temporary language files
        import json
        with open("temp_en.json", "w", encoding="utf-8") as f:
            json.dump(english_custom, f, ensure_ascii=False, indent=2)
        with open("temp_de.json", "w", encoding="utf-8") as f:
            json.dump(german_custom, f, ensure_ascii=False, indent=2)
            
        # Add language packages
        self.language.AddLanguagePackage("en", "temp_en.json")
        self.language.AddLanguagePackage("de", "temp_de.json")
        self.language.Reload()
        
    def demonstrate_languages(self):
        """Show the app in different languages"""
        
        languages = ["en", "de", "ru", "fr"]
        
        for lang in languages:
            print(f"\n{'='*50}")
            print(f"🌍 LANGUAGE: {lang.upper()}")
            print(f"{'='*50}")
            
            # Switch language
            self.Settings.LANGUAGE = lang
            self.language.Reload()
            
            # Show translations
            print(f"📝 {self.language.Translate('app_welcome')}")
            print(f"🔧 {self.language.Translate('language_demo')}")
            print(f"✨ {self.language.Translate('custom_message')}")
            
            # Show built-in vocabulary
            print(f"🔄 Built-in terms:")
            print(f"   - Settings: {self.language.Translate('settings')}")
            print(f"   - Save: {self.language.Translate('save')}")
            print(f"   - Exit: {self.language.Translate('exit')}")
            print(f"   - Welcome: {self.language.Translate('welcome')}")
            
            print(f"👋 {self.language.Translate('goodbye_message')}")
            
    def cleanup(self):
        """Clean up temporary files"""
        import os
        for file in ["temp_en.json", "temp_de.json"]:
            if os.path.exists(file):
                os.remove(file)

def main():
    print("🚀 ToolOS SDK - Basic Multi-Language Example")
    print("=" * 60)
    
    app = BasicMultiLangApp()
    
    try:
        app.demonstrate_languages()
        
        print(f"\n{'='*60}")
        print("✅ Demo completed successfully!")
        print(f"📊 Available languages: {app.language.GetAvailableLanguages()}")
        print(f"🔑 Total translation keys: {len(app.language.GetAllTranslationKeys())}")
        
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()