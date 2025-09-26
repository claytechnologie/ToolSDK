import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks_file = "data/assets/cache/tasks.json"
        self.tasks = self.load_tasks()
        self.isRunning = False
        self.MENU = [
            "📝 Neue Aufgabe hinzufügen",
            "📋 Alle Aufgaben anzeigen", 
            "✅ Aufgabe als erledigt markieren",
            "🗑️ Aufgabe löschen",
            "📊 Statistiken anzeigen",
            "🚪 Zurück zum Hauptmenü"
        ]
    
    def load_tasks(self):
        """Lädt Aufgaben aus der JSON-Datei"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self):
        """Speichert Aufgaben in die JSON-Datei"""
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_header(self):
        print("=" * 50)
        print("📋 TASK MANAGER v1.0")
        print("=" * 50)
        print()
    
    def show_menu(self):
        for i, option in enumerate(self.MENU):
            print(f"{i}. {option}")
        print()
    
    def add_task(self):
        """Neue Aufgabe hinzufügen"""
        self.clear_console()
        self.show_header()
        print("📝 NEUE AUFGABE HINZUFÜGEN\n")
        
        title = input("Aufgaben-Titel: ").strip()
        if not title:
            print("❌ Titel darf nicht leer sein!")
            input("Drücken Sie Enter...")
            return
        
        description = input("Beschreibung (optional): ").strip()
        priority = input("Priorität (hoch/mittel/niedrig): ").strip().lower()
        
        if priority not in ['hoch', 'mittel', 'niedrig']:
            priority = 'mittel'
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'completed': False,
            'created': datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Aufgabe '{title}' wurde hinzugefügt!")
        input("Drücken Sie Enter...")
    
    def show_tasks(self):
        """Alle Aufgaben anzeigen"""
        self.clear_console()
        self.show_header()
        print("📋 ALLE AUFGABEN\n")
        
        if not self.tasks:
            print("📭 Keine Aufgaben vorhanden.")
            input("Drücken Sie Enter...")
            return
        
        for task in self.tasks:
            status = "✅" if task['completed'] else "⏳"
            priority_icon = {"hoch": "🔴", "mittel": "🟡", "niedrig": "🟢"}.get(task['priority'], "⚪")
            
            print(f"{status} [{task['id']}] {priority_icon} {task['title']}")
            if task['description']:
                print(f"    📝 {task['description']}")
            print(f"    📅 Erstellt: {task['created']}")
            print("-" * 40)
        
        input("\nDrücken Sie Enter...")
    
    def complete_task(self):
        """Aufgabe als erledigt markieren"""
        self.clear_console()
        self.show_header()
        print("✅ AUFGABE ALS ERLEDIGT MARKIEREN\n")
        
        if not self.tasks:
            print("📭 Keine Aufgaben vorhanden.")
            input("Drücken Sie Enter...")
            return
        
        # Unerledigte Aufgaben anzeigen
        pending_tasks = [t for t in self.tasks if not t['completed']]
        if not pending_tasks:
            print("🎉 Alle Aufgaben bereits erledigt!")
            input("Drücken Sie Enter...")
            return
        
        print("Unerledigte Aufgaben:")
        for task in pending_tasks:
            priority_icon = {"hoch": "🔴", "mittel": "🟡", "niedrig": "🟢"}.get(task['priority'], "⚪")
            print(f"[{task['id']}] {priority_icon} {task['title']}")
        
        try:
            task_id = int(input("\nAufgaben-ID zum Markieren: "))
            for task in self.tasks:
                if task['id'] == task_id and not task['completed']:
                    task['completed'] = True
                    task['completed_date'] = datetime.now().strftime("%d.%m.%Y %H:%M")
                    self.save_tasks()
                    print(f"✅ Aufgabe '{task['title']}' als erledigt markiert!")
                    input("Drücken Sie Enter...")
                    return
            print("❌ Aufgabe nicht gefunden oder bereits erledigt!")
        except ValueError:
            print("❌ Ungültige ID!")
        
        input("Drücken Sie Enter...")
    
    def delete_task(self):
        """Aufgabe löschen"""
        self.clear_console()
        self.show_header()
        print("🗑️ AUFGABE LÖSCHEN\n")
        
        if not self.tasks:
            print("📭 Keine Aufgaben vorhanden.")
            input("Drücken Sie Enter...")
            return
        
        print("Alle Aufgaben:")
        for task in self.tasks:
            status = "✅" if task['completed'] else "⏳"
            priority_icon = {"hoch": "🔴", "mittel": "🟡", "niedrig": "🟢"}.get(task['priority'], "⚪")
            print(f"{status} [{task['id']}] {priority_icon} {task['title']}")
        
        try:
            task_id = int(input("\nAufgaben-ID zum Löschen: "))
            for i, task in enumerate(self.tasks):
                if task['id'] == task_id:
                    deleted_title = task['title']
                    del self.tasks[i]
                    self.save_tasks()
                    print(f"🗑️ Aufgabe '{deleted_title}' wurde gelöscht!")
                    input("Drücken Sie Enter...")
                    return
            print("❌ Aufgabe nicht gefunden!")
        except ValueError:
            print("❌ Ungültige ID!")
        
        input("Drücken Sie Enter...")
    
    def show_statistics(self):
        """Statistiken anzeigen"""
        self.clear_console()
        self.show_header()
        print("📊 STATISTIKEN\n")
        
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        pending_tasks = total_tasks - completed_tasks
        
        print(f"📋 Gesamt: {total_tasks}")
        print(f"✅ Erledigt: {completed_tasks}")
        print(f"⏳ Offen: {pending_tasks}")
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"📈 Completion Rate: {completion_rate:.1f}%")
            
            # Prioritäten-Statistik
            priorities = {}
            for task in self.tasks:
                priorities[task['priority']] = priorities.get(task['priority'], 0) + 1
            
            print("\n🎯 Nach Priorität:")
            for priority, count in priorities.items():
                icon = {"hoch": "🔴", "mittel": "🟡", "niedrig": "🟢"}.get(priority, "⚪")
                print(f"  {icon} {priority.capitalize()}: {count}")
        
        input("\nDrücken Sie Enter...")
    
    def start(self):
        """Hauptmenü starten"""
        self.isRunning = True
        
        while self.isRunning:
            self.clear_console()
            self.show_header()
            self.show_menu()
            
            try:
                choice = int(input("Wählen Sie eine Option: "))
                
                if choice == 0:
                    self.add_task()
                elif choice == 1:
                    self.show_tasks()
                elif choice == 2:
                    self.complete_task()
                elif choice == 3:
                    self.delete_task()
                elif choice == 4:
                    self.show_statistics()
                elif choice == 5:
                    print("🚪 Zurück zum Hauptmenü...")
                    self.isRunning = False
                else:
                    print("❌ Ungültige Auswahl!")
                    input("Drücken Sie Enter...")
                    
            except ValueError:
                print("❌ Bitte geben Sie eine gültige Zahl ein!")
                input("Drücken Sie Enter...")

# Diese Funktion wird vom Hauptsystem aufgerufen
def start():
    """Entry Point für das Mod-System"""
    task_manager = TaskManager()
    task_manager.start()

# Für direkten Start (während der Entwicklung)
if __name__ == "__main__":
    start()