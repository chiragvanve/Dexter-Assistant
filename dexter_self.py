import os
import json
import shutil

class AeroSentinel:
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.files = ["dexter_main.py",
                      "sentinel_ui.py",
                      "dexter_logic.py",
                      "dexter_self.py",
                      "dexter_hand.py", 
                      "dexter_eyes.py"]
        self.memory_file = os.path.join(self.directory, "aero_memory.json")
        
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({}, f)

    def recover(self, filename):
        """Swaps the .bak file back to .py if the system crashes."""
        path = os.path.join(self.directory, filename)
        bak_path = path + ".bak"
        if os.path.exists(bak_path):
            shutil.copy(bak_path, path)
            return True
        return False

    def evolve(self, filename, new_code):
        path = os.path.join(self.directory, filename)
        # Always backup before writing
        current_code = self.get_my_code(filename)
        if current_code:
            with open(path + ".bak", 'w') as b:
                b.write(current_code)
        
        with open(path, 'w') as f:
            f.write(new_code)
        return True

    def get_my_code(self, filename):
        path = os.path.join(self.directory, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return None

    def get_all_memories(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except: return {}

    def remember(self, key, value):
        data = self.get_all_memories()
        data[key] = value
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Logged: {value}"
