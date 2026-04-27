import speech_recognition as sr
import logging

class DexterEars:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # --- ELITE ACOUSTIC TUNING ---
        # How long to wait after a phrase before processing (1.5s = natural breath)
        self.recognizer.pause_threshold = 1.5 
        
        # How much silence is allowed inside a phrase
        self.recognizer.phrase_threshold = 0.3
        
        # Initial sensitivity (will be tuned by calibrator)
        self.recognizer.energy_threshold = 400 
        self.recognizer.dynamic_energy_threshold = True
        
        logging.info("🎧 Ears: Initialization complete.")

    def calibrate(self):
        """God-Level: Profiles the room's background noise to set the perfect baseline."""
        with sr.Microphone() as source:
            print("🎧 Ears: Calibrating for background noise... (Keep quiet for 1 sec)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"✅ Baseline Set: {self.recognizer.energy_threshold:.2f}")

    def listen_for_command(self):
        with sr.Microphone() as source:
            print("🟢 Ears: Listening...")
            try:
                # listen(source, timeout, phrase_time_limit)
                # We give you 5 seconds to start talking, and 12 seconds to finish.
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=12)
                
                print("🟡 Ears: Translating audio to logic...")
                # Using Google's engine (requires internet)
                text = self.recognizer.recognize_google(audio)
                return text
                
            except sr.WaitTimeoutError:
                print("⚠️ Ears: No speech detected (Timeout).")
                return None
            except sr.UnknownValueError:
                print("⚠️ Ears: Sound detected, but couldn't resolve words.")
                return None
            except Exception as e:
                print(f"❌ Ears: Hardware Error: {e}")
                return None
