import pygame
import os
import time
import subprocess
import sys

class DexterVoice:
    def __init__(self):
        print("🗣️ Vocal Cords: Initializing Neural Engine...")
        # Initialize mixer with a high frequency for crisp audio
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.voice = "en-GB-RyanNeural"
        
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.audio_path = os.path.join(self.directory, "dexter_speech.mp3")
        self.text_path = os.path.join(self.directory, "dexter_temp_text.txt")

    def speak(self, text):
        if not text or not text.strip(): return
        
        try:
            # 1. Clean up old artifacts (Force Unlock if necessary)
            for f in [self.audio_path, self.text_path]:
                if os.path.exists(f):
                    try: os.remove(f)
                    except: pass
            
            # 2. Secure Write (Handles special characters for E&TC terms)
            with open(self.text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # 3. Trigger Neural Synthesis
            cmd = [
                sys.executable, "-m", "edge_tts", 
                "--voice", self.voice, 
                "-f", self.text_path, 
                "--write-media", self.audio_path
            ]
            
            subprocess.run(cmd, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # 4. THE GOD-LEVEL SYNC: Wait for Disk IO
            timeout = 0
            while not os.path.exists(self.audio_path) and timeout < 20:
                time.sleep(0.1) # Check every 100ms
                timeout += 1

            if not os.path.exists(self.audio_path):
                print("❌ Voice Error: Mp3 synthesis timed out.")
                return

            # 5. High-Fidelity Playback
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()
            
            # Keep thread alive while speaking
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # 6. Smooth Release & Cleanup
            pygame.mixer.music.unload()
            time.sleep(0.1) # Breathable gap
            
            for f in [self.audio_path, self.text_path]:
                if os.path.exists(f):
                    try: os.remove(f)
                    except: pass
                    
        except subprocess.CalledProcessError:
            print(f"🎙️ CLI Error: edge-tts check failed. Ensure internet is active.")
        except Exception as e:
            print(f"🎙️ Voice Engine Error: {e}")
