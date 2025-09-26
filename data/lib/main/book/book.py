import json
import os
from datetime import datetime

class Tagebuch:
    def __init__(self):
        self.isRunning = False
        self.MENU = ["📝 Eintrag hinzufügen", "📖 Einträge anzeigen", "🔍 Eintrag suchen", "🗑️ Eintrag löschen", "🚪 Beenden"]
        self.diary_file = "data/assets/cache/diary.json"
        self.entries = self.load_entries()

    def load_entries(self):
        """Lädt Tagebucheinträge aus der JSON-Datei"""
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_entries(self):
        """Speichert Tagebucheinträge in die JSON-Datei"""
        os.makedirs(os.path.dirname(self.diary_file), exist_ok=True)
        with open(self.diary_file, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self):
        print("=" * 50)
        print("📖 MEIN TAGEBUCH")
        print("=" * 50)
        print()

    def start(self):
        self.isRunning = True
        
        while self.isRunning:
            self.clear_console()
            self.show_header()
            self.show_menu()
            
            try:
                self.ProcessAction(int(input("Wähle eine Option: ")))
            except ValueError:
                print("❌ Bitte geben Sie eine gültige Zahl ein!")
                input("Drücken Sie Enter...")

    def show_menu(self):
        for i, option in enumerate(self.MENU):
            print(f"{i}. {option}")
        print()
            
    def ProcessAction(self, selection: int):
        if selection == 0:
            self.add_entry()
        elif selection == 1:
            self.show_entries()
        elif selection == 2:
            self.search_entries()
        elif selection == 3:
            self.delete_entry()
        elif selection == 4:
            self.isRunning = False
            print("🚪 Beende das Tagebuch...")
        else:
            print("❌ Ungültige Auswahl. Bitte versuche es erneut.")
            input("Drücken Sie Enter...")

    def add_entry(self):
        """Fügt einen neuen Tagebucheintrag hinzu"""
        self.clear_console()
        self.show_header()
        print("📝 NEUER TAGEBUCHEINTRAG\n")
        
        title = input("Titel des Eintrags: ").strip()
        if not title:
            print("❌ Titel darf nicht leer sein!")
            input("Drücken Sie Enter...")
            return
        
        print("Inhalt des Eintrags (Beenden mit leerer Zeile):")
        content_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines)
        if not content:
            print("❌ Inhalt darf nicht leer sein!")
            input("Drücken Sie Enter...")
            return
        
        # Stimmung hinzufügen
        print("\nWie war deine Stimmung heute?")
        moods = ["😄 Sehr gut", "😊 Gut", "😐 Neutral", "😔 Schlecht", "😢 Sehr schlecht"]
        for i, mood in enumerate(moods):
            print(f"{i}. {mood}")
        
        try:
            mood_choice = int(input("Stimmung wählen (0-4): "))
            if 0 <= mood_choice < len(moods):
                mood = moods[mood_choice].split()[0]  # Nur das Emoji
            else:
                mood = "😐"
        except ValueError:
            mood = "😐"
        
        entry = {
            'id': len(self.entries) + 1,
            'title': title,
            'content': content,
            'mood': mood,
            'date': datetime.now().strftime("%d.%m.%Y"),
            'time': datetime.now().strftime("%H:%M"),
            'timestamp': datetime.now().isoformat()
        }
        
        self.entries.append(entry)
        self.save_entries()
        print(f"\n✅ Eintrag '{title}' wurde gespeichert!")
        input("Drücken Sie Enter...")

    def show_entries(self):
        """Zeigt alle Tagebucheinträge an"""
        self.clear_console()
        self.show_header()
        print("📖 ALLE TAGEBUCHEINTRÄGE\n")
        
        if not self.entries:
            print("📭 Noch keine Einträge vorhanden.")
            print("Tipp: Fügen Sie über Option 0 einen neuen Eintrag hinzu!")
            input("Drücken Sie Enter...")
            return
        
        # Sortiere Einträge nach Datum (neueste zuerst)
        sorted_entries = sorted(self.entries, key=lambda x: x['timestamp'], reverse=True)
        
        for i, entry in enumerate(sorted_entries):
            print(f"📝 {entry['mood']} [{entry['id']}] {entry['title']}")
            print(f"📅 {entry['date']} um {entry['time']}")
            print("─" * 40)
            
            # Zeige ersten Teil des Inhalts
            content_preview = entry['content'][:100]
            if len(entry['content']) > 100:
                content_preview += "..."
            print(content_preview)
            print("─" * 40)
            
            # Nach jedem 3. Eintrag fragen ob weiter
            if (i + 1) % 3 == 0 and i + 1 < len(sorted_entries):
                choice = input(f"\n[{i+1}/{len(sorted_entries)}] Weitere Einträge anzeigen? (j/n): ").lower()
                if choice != 'j':
                    break
                print()
        
        print(f"\n📊 Gesamt: {len(self.entries)} Einträge")
        input("Drücken Sie Enter...")

    def search_entries(self):
        """Sucht in Tagebucheinträgen"""
        self.clear_console()
        self.show_header()
        print("🔍 EINTRÄGE DURCHSUCHEN\n")
        
        if not self.entries:
            print("📭 Keine Einträge zum Durchsuchen vorhanden.")
            input("Drücken Sie Enter...")
            return
        
        search_term = input("Suchbegriff eingeben: ").strip().lower()
        if not search_term:
            print("❌ Suchbegriff darf nicht leer sein!")
            input("Drücken Sie Enter...")
            return
        
        # Suche in Titel und Inhalt
        found_entries = []
        for entry in self.entries:
            if (search_term in entry['title'].lower() or 
                search_term in entry['content'].lower()):
                found_entries.append(entry)
        
        if not found_entries:
            print(f"❌ Keine Einträge mit '{search_term}' gefunden.")
        else:
            print(f"🔍 {len(found_entries)} Einträge mit '{search_term}' gefunden:\n")
            
            for entry in found_entries:
                print(f"📝 {entry['mood']} [{entry['id']}] {entry['title']}")
                print(f"📅 {entry['date']} um {entry['time']}")
                
                # Highlight des Suchbegriffs
                content_lines = entry['content'].split('\n')
                for line in content_lines[:3]:  # Zeige nur erste 3 Zeilen
                    if search_term in line.lower():
                        print(f"💡 ...{line}...")
                        break
                print("-" * 30)
        
        input("Drücken Sie Enter...")

    def delete_entry(self):
        """Löscht einen Tagebucheintrag"""
        self.clear_console()
        self.show_header()
        print("🗑️ EINTRAG LÖSCHEN\n")
        
        if not self.entries:
            print("📭 Keine Einträge zum Löschen vorhanden.")
            input("Drücken Sie Enter...")
            return
        
        print("Verfügbare Einträge:")
        for entry in self.entries:
            print(f"[{entry['id']}] {entry['mood']} {entry['title']} ({entry['date']})")
        
        try:
            entry_id = int(input("\nEintags-ID zum Löschen: "))
            
            for i, entry in enumerate(self.entries):
                if entry['id'] == entry_id:
                    title = entry['title']
                    confirm = input(f"Wirklich '{title}' löschen? (ja/nein): ").lower()
                    
                    if confirm in ['ja', 'j', 'yes', 'y']:
                        del self.entries[i]
                        self.save_entries()
                        print(f"🗑️ Eintrag '{title}' wurde gelöscht!")
                    else:
                        print("❌ Löschung abgebrochen.")
                    
                    input("Drücken Sie Enter...")
                    return
            
            print("❌ Eintrag nicht gefunden!")
        except ValueError:
            print("❌ Ungültige ID!")
        
        input("Drücken Sie Enter...")

def start():
    book = Tagebuch()
    book.start()