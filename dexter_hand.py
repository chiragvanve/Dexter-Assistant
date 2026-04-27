import pyautogui
import pyperclip
import time
import logging
from youtube_transcript_api import YouTubeTranscriptApi

class DexterActions:
    def __init__(self):
        logging.info("🦾 Physical Layer: Dexter Hands Online.")

    def execute(self, action):
        """Routes the physical action."""
        if action == "summarize_youtube":
            return self._extract_and_summarize_yt()
        
        # ... [Your other actions like "open sekiro" can stay here] ...
        
        return f"ACTION '{action}' EXECUTED."

    def _extract_and_summarize_yt(self):
        """God-Level: Grabs the URL from Brave and extracts the transcript."""
        try:
            # 1. Grab the URL from the active browser window
            pyautogui.hotkey('ctrl', 'l')  # Focus the address bar
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')  # Copy the URL
            time.sleep(0.2)
            pyautogui.press('esc')         # Deselect the address bar
            
            url = pyperclip.paste()

            if "youtube.com/watch" not in url:
                return "COULD NOT DETECT A VALID YOUTUBE VIDEO LINK."

            # 2. Extract the Video ID
            # Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ -> dQw4w9WgXcQ
            video_id = url.split("v=")[1].split("&")[0]

            # 3. Rip the Transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine the first 50 lines of text (to avoid overloading the TTS)
            text_blocks = [t['text'] for t in transcript_list[:50]]
            raw_text = " ".join(text_blocks)
            
            # Note: For the final build, we will pass 'raw_text' to dexter_logic for an AI summary.
            # For now, he will report the data capture.
            word_count = len(raw_text.split())
            
            return f"TRANSCRIPT EXTRACTED. THE VIDEO STARTS WITH: {raw_text[:100]}..."

        except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
            return "COULD NOT EXTRACT TRANSCRIPT. CAPTIONS MIGHT BE DISABLED FOR THIS VIDEO."
        except Exception as e:
            logging.error(f"YouTube Rip Error: {e}")
            return "ENCOUNTERED AN ERROR WHILE EXTRACTING VIDEO DATA."
