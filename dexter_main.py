import sys
import io
import threading
import time
import queue
import keyboard
import random
import re
import os
import psutil
import logging
from concurrent.futures import ThreadPoolExecutor

# ── SYSTEM ENCODING GATEWAY ──
# Force Windows Terminal to handle UTF-8 clean logs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ── LOGGING INFRASTRUCTURE ──
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] DexterCore: %(message)s',
    handlers=[
        logging.FileHandler("dexter_system.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# ── CORE NERVOUS SYSTEM IMPORTS ──
try:
    from sentinel_ui import SentinelIsland 
    from dexter_voice import DexterVoice
    from dexter_ears import DexterEars
    from dexter_logic import DexterBrain 
    from dexter_self import AeroSentinel 
    from dexter_hand import DexterActions 
    from dexter_eyes import DexterVision 
except ImportError as e:
    print(f"🚨 CRITICAL SYSTEM FAILURE: Missing Module -> {e}")
    sys.exit(1)

# ── SYSTEM HEALTH ENGINE ──
def get_system_report():
    """Generates professional telemetry data for the Victus laptop."""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        report = f"SYSTEM ONLINE. CPU AT {cpu}%. RAM AT {ram}%. "
        if battery:
            report += f"BATTERY IS AT {battery.percent}% AND {'CHARGING' if battery.power_plugged else 'ON DC'}."
        return report
    except Exception as e:
        logging.error(f"Telemetry Error: {e}")
        return "SYSTEM ONLINE. TELEMETRY UNAVAILABLE."

# ── MAIN ASSISTANT ENTITY ──
class DexterAssistant:
    def __init__(self):
        # 1. UI & Visual Layer (Passes self to hook into UI interactions)
        self.ui = SentinelIsland(self) 
        
        # 2. Audio Layer
        self.voice = DexterVoice()
        self.ears = DexterEars()
        
        # 3. Cognitive & Physical Layers
        self.brain = DexterBrain()
        self.self_layer = AeroSentinel()
        self.hands = DexterActions()
        self.eyes = DexterVision()
        
        # 4. Multithreaded Nervous System
        self.ui_q = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.is_busy = False
        self.pending_action = None

    def tell(self, text, duration=0):
        """Syncs Frosted HUD with Neural TTS."""
        if not text: return
        logging.info(f"DEXTER: {text}")
        
        # Format for Frosted HUD
        disp_time = max(3500, len(text) * 80) if duration == 0 else duration
        self.ui_q.put((text, disp_time))
        
        # Threaded Voice Playback
        self.executor.submit(self.voice.speak, text)

    def update_ui_loop(self):
        """HUD Refresh Cycle (100ms)"""
        while not self.ui_q.empty():
            try:
                msg, dur = self.ui_q.get_nowait()
                self.ui.trigger_pop(msg, dur)
            except: break
        self.ui.root.after(100, self.update_ui_loop)

    def proactive_observer(self):
        """The 'Eyes' Thread: Monitors Victus screen context."""
        while True:
            if not self.is_busy and not self.pending_action:
                screen_data = self.eyes.glance()
                if screen_data:
                    self.handle_vision_logic(screen_data)
            time.sleep(30)

    def handle_vision_logic(self, text):
        """Processes visual data while filtering for recursive loops."""
        t_low = text.lower()
        
        # Prevent Dexter from trying to 'fix' his own terminal text
        if "dextercore" in t_low or "vocal cords" in t_low:
            return

        if "youtube.com" in t_low:
            self.pending_action = "summarize_youtube"
            self.ui.update_status("SIGHT DETECTED", is_active=True)
            self.tell("YOUTUBE DETECTED. ANALYZE CONTENT?")
        else:
            errs = self.eyes.look_for_errors(text)
            if errs:
                self.pending_action = f"fix:{errs[0]}"
                self.ui.update_status("ERROR DETECTED", is_active=True)
                self.tell(f"I SEE A {errs[0]} ALERT. DEPLOY FIX?")

    def process(self, voice_mode=True, text_input=""):
        """Accepts either Voice or Typed Input from the HUD."""
        if self.is_busy: return
        self.is_busy = True

        try:
            # Check if this is a typed command or voice command
            if text_input:
                self.ui.update_status("PROCESSING", is_active=True)
                cmd = text_input # Use the text passed from the UI
            else:
                self.ui.update_status("LISTENING", is_active=True)
                cmd = self.ears.listen_for_command() 

            if cmd:
                cmd_l = re.sub(r'[^\w\s]', '', cmd.lower()).strip()
                self.ui.update_status("THINKING", is_active=True)

                # 1. CONFIRMATION GATEWAY
                if self.pending_action:
                    confirmations = ["yes", "do it", "confirm", "sure", "yep", "y"]
                    if any(word == cmd_l for word in confirmations) or "yes" in cmd_l:
                        self.ui.update_status("EXECUTING", is_active=True)
                        res = self.hands.execute(self.pending_action)
                        self.tell(res)
                    else:
                        self.tell("STANDING DOWN.")
                    self.pending_action = None
                    return

                # 2. COMMAND ROUTING
                triggers = ["open", "launch", "search", "play", "go to"]
                if any(t in cmd_l for t in triggers):
                    self.pending_action = cmd_l
                    self.tell(f"CONFIRM: {cmd_l}?")
                else:
                    res = self.brain.think(cmd, self.self_layer.get_all_memories())
                    self.tell(res)

        except Exception as e:
            logging.error(f"Input crash: {e}")
            self.tell("COULD NOT PROCESS COMMAND.")

        finally:
            self.ui.update_status("STANDBY", is_active=False)
            self.is_busy = False

    def start(self):
        """Professional Ignition Sequence."""
        # 1. Link Left-Click to Voice Mode
        self.ui.external_trigger = self.process 
        # 2. Link the Text Box to Text Mode
        self.ui.external_text_trigger = lambda text_input: self.process(voice_mode=False, text_input=text_input)
        
        # Launch background nervous system
        threading.Thread(target=self.proactive_observer, daemon=True).start()
        threading.Thread(target=self.kb_listener, daemon=True).start()
        
        self.ui.root.after(100, self.update_ui_loop)
        
        # Generate the hardware report on boot
        def run_report():
            report = get_system_report()
            self.tell("DEXTER ONLINE. " + report)
            
        self.ui.root.after(1500, run_report)
        self.ui.loop()

    def kb_listener(self):
        """Global hotkeys for the Victus."""
        while True:
            if keyboard.is_pressed('num 5'): 
                self.process(voice_mode=True)
                time.sleep(1.2)
            if keyboard.is_pressed('num 6'): 
                # Use .after to safely tell the UI thread to open the text box
                self.ui.root.after(0, self.ui.enable_typing)
                time.sleep(1.2)
            time.sleep(0.1)

if __name__ == "__main__":
    DexterAssistant().start()
# ── SYSTEM HEALTH ENGINE ──
def get_system_report():
    """Generates professional, concise telemetry data."""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        report = f"CPU {cpu}%, RAM {ram}%."
        if battery:
            pwr_status = "CHARGING" if battery.power_plugged else "ON DC"
            report += f" PWR: {battery.percent}% ({pwr_status})."
        return report
    except Exception as e:
        logging.error(f"Telemetry Error: {e}")
        return "TELEMETRY UNAVAILABLE."

