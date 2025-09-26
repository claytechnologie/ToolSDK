class ModLoader:
    
    def __init__(self, settings):
        import os
        self.os = os
        import json
        self.js = json
        self.settings = settings
        self.MODPATH = settings.Global("modpath")
        self.AUTHORIZED = {
            "id": settings.Global("authorized_ids") # Always allowed IDs
        }
        
        # Prüfe ob MODPATH existiert, wenn nicht erstelle es
        if not os.path.exists(self.MODPATH):
            print(f"Mod directory nicht gefunden: {self.MODPATH}")
            print("Erstelle Mod-Verzeichnis...")
            os.makedirs(self.MODPATH, exist_ok=True)
            self.MODS = []
        else:
            self.MODS = os.listdir(self.MODPATH)
            
        self.AVAILABLE_MODS = self.CheckMods()
        self.MODDED = []
        self.ReadMods()
        
        
        
    def ReadMods(self):
        for mod in self.AVAILABLE_MODS:
            path = self.os.path.join(self.MODPATH, mod)
            if self.os.path.isdir(path):
                content = self.os.listdir(path)
                if "package.json" in content:
                    package_path = self.os.path.join(path, "package.json")
                    with open(package_path, "r") as f:
                        data = self.js.load(f)
                        build = data.get("build", {})
                        if x:= build.get("source"):
                            if y:= build.get("mesh"):
                                if z:= build.get("action"):
                                    if w:= build.get("path"):
                                        self.MODDED.append({
                                            "name": mod,
                                            "mesh": y,
                                            "build": build,
                                            "action": z,
                                            "path": w,
                                        })
                                
                                
        
        
    def CheckMods(self):
        try:
            for mod in self.MODS:
                mod_path = self.os.path.join(self.MODPATH, mod)
                if not self.os.path.isdir(mod_path):
                    continue
                    
                content = self.os.listdir(mod_path)
                if "package.json" in content:
                    package_path = self.os.path.join(mod_path, "package.json")
                    with open(package_path, "r") as f:
                        data = self.js.load(f)
                        
                        mod_id = data.get("id")
                        if mod_id and mod_id in self.AUTHORIZED['id']:
                            yield mod
                    
        except Exception as e:
            return
                    