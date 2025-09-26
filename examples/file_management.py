"""
ToolOS SDK - File Management Example
====================================

This example demonstrates:
- Cache API usage
- Temp API usage  
- Log API usage
- File operations with UTF-8 support
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.assets.api.tool_api import ToolAPI
import json
import time

class FileManagementDemo(ToolAPI):
    
    def __init__(self):
        super().__init__(name="FileDemo", version="1.0.0")
        
    def demonstrate_cache_api(self):
        """Demonstrate Cache API functionality"""
        print("🗄️  CACHE API DEMONSTRATION")
        print("-" * 40)
        
        # Write cache data
        cache_data = {
            "user_preferences": {
                "language": "en",
                "theme": "dark",
                "notifications": True
            },
            "session_info": {
                "login_time": time.time(),
                "user_id": "12345"
            }
        }
        
        self.Cache.WriteCacheFile("user_session.json", json.dumps(cache_data, indent=2))
        print("✅ Cache file written: user_session.json")
        
        # Read cache data
        cached_content = self.Cache.ReadCacheFile("user_session.json")
        print("📖 Cache content loaded successfully")
        
        # Add content to cache
        self.Cache.AddContent("app_log.txt", f"Cache demo completed at {time.ctime()}")
        print("➕ Content added to cache log")
        
        return cached_content
        
    def demonstrate_temp_api(self):
        """Demonstrate Temp API functionality"""
        print("\n🔄 TEMP API DEMONSTRATION")
        print("-" * 40)
        
        # Create temporary processing data
        temp_data = {
            "processing_id": "temp_001",
            "status": "in_progress",
            "data": ["item1", "item2", "item3"],
            "timestamp": time.time()
        }
        
        self.Temp.WriteTempFile("processing.json", json.dumps(temp_data, indent=2))
        print("✅ Temp file created: processing.json")
        
        # Check if temp file exists
        if self.Temp.TempExists("processing.json"):
            print("✅ Temp file existence confirmed")
            
            # Read temp data
            temp_content = self.Temp.ReadTempFile("processing.json")
            print("📖 Temp content loaded")
            
            # Add processing logs
            for i in range(3):
                self.Temp.AddContent("process_log.txt", f"Processing step {i+1} completed")
                time.sleep(0.1)  # Simulate processing time
                
            print("➕ Processing logs added to temp")
            
        return temp_content
        
    def demonstrate_log_api(self):
        """Demonstrate Log API functionality"""
        print("\n📝 LOG API DEMONSTRATION")
        print("-" * 40)
        
        # Log different types of events
        events = [
            "Application started successfully",
            "User authentication completed",
            "Cache system initialized", 
            "Processing 100 items...",
            "⚠️  Warning: High memory usage detected",
            "🎉 Processing completed successfully!",
            "🌍 Multi-language support: Mehrsprachige Unterstützung aktiviert!",
            "🇷🇺 Russian support: Поддержка русского языка активирована!",
            "Application shutdown initiated"
        ]
        
        for event in events:
            self.Log.WriteLog("file_demo.log", event)
            time.sleep(0.05)  # Simulate real-time logging
            
        print("✅ 9 log entries written with UTF-8 support")
        
        # Read and display log
        log_content = self.Log.ReadLog("file_demo.log")
        print("\n📖 LOG CONTENT PREVIEW (last 3 lines):")
        log_lines = log_content.strip().split('\n')
        for line in log_lines[-3:]:
            print(f"   {line}")
            
        return log_content
        
    def demonstrate_multilingual_logging(self):
        """Show multilingual logging capabilities"""  
        print("\n🌍 MULTILINGUAL LOGGING")
        print("-" * 40)
        
        languages = ["en", "de", "ru", "fr"]
        
        for lang in languages:
            self.Settings.LANGUAGE = lang
            self.language.Reload()
            
            # Log in current language
            welcome_msg = self.language.Translate("welcome")
            settings_msg = self.language.Translate("settings")
            
            self.Log.WriteLog("multilang.log", f"[{lang.upper()}] {welcome_msg}")
            self.Log.WriteLog("multilang.log", f"[{lang.upper()}] {settings_msg}")
            
        print("✅ Multilingual logs created in 4 languages")
        
    def show_file_statistics(self):
        """Display file operation statistics"""
        print("\n📊 FILE OPERATION STATISTICS")
        print("-" * 40)
        
        # Count log entries
        log_content = self.Log.ReadLog("file_demo.log")
        log_lines = len(log_content.strip().split('\n'))
        
        multilang_content = self.Log.ReadLog("multilang.log")
        multilang_lines = len(multilang_content.strip().split('\n'))
        
        print(f"📝 Main log entries: {log_lines}")
        print(f"🌍 Multilang log entries: {multilang_lines}")
        print(f"🗄️  Cache files created: 2")
        print(f"🔄 Temp files created: 2")
        print(f"📁 Total file operations: {log_lines + multilang_lines + 4}")

def main():
    print("🚀 ToolOS SDK - File Management Demo")
    print("=" * 60)
    
    demo = FileManagementDemo()
    
    try:
        # Run demonstrations
        cached_data = demo.demonstrate_cache_api()
        temp_data = demo.demonstrate_temp_api()
        log_data = demo.demonstrate_log_api()
        demo.demonstrate_multilingual_logging()
        demo.show_file_statistics()
        
        print(f"\n{'='*60}")
        print("✅ File Management Demo completed successfully!")
        print("📁 Check the following directories for created files:")
        print(f"   - Cache: {demo.Settings.CACHEPATH}")
        print(f"   - Temp: {demo.Settings.TEMPPATH}")
        print(f"   - Logs: {demo.Settings.LOGPATH}")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    main()