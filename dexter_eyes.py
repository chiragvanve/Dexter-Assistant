import cv2
import pyautogui
import pytesseract
import logging
from ultralytics import YOLO

class DexterVision:
    def __init__(self):
        # 1. Initialize OCR (Screen Sight)
        # Ensure this path matches your Tesseract installation
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # 2. Initialize YOLOv8 (Physical Sight)
        # This is lightweight and usually installs without C++ errors
        try:
            self.model = YOLO('yolov8n.pt') 
            self.vision_active = True
        except Exception as e:
            logging.error(f"👁️ YOLO Load Failed: {e}")
            self.vision_active = False
            
        logging.info("👁️ Optics: Lean Neural Vision Initialized (dlib-free).")

    def glance(self):
        """High-Speed Screen OCR for error detection."""
        try:
            screenshot = pyautogui.screenshot()
            text = pytesseract.image_to_string(screenshot)
            return text
        except Exception as e:
            logging.error(f"👁️ Screen Sight Failure: {e}")
            return None

    def live_scan(self, duration=3):
        """Webcam Perception: Identifies objects in your room."""
        if not self.vision_active:
            return ["Vision system offline"]

        cap = cv2.VideoCapture(0)
        found_objects = set()
        start_time = cv2.getTickCount() / cv2.getTickFrequency()

        while (cv2.getTickCount() / cv2.getTickFrequency() - start_time) < duration:
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model(frame, verbose=False)
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    found_objects.add(self.model.names[cls])

        cap.release()
        return list(found_objects)

    def verify_user(self):
        """Simplified Security: Checks if a 'person' is present."""
        # Instead of face recognition, we just check for a human figure
        if not self.vision_active: return True
        
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if not ret: return True # Failsafe
        
        results = self.model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                if self.model.names[int(box.cls[0])] == 'person':
                    return True
        return False

    def look_for_errors(self, screen_text):
        """Scans for system errors with loop prevention."""
        if not screen_text or "DexterCore" in screen_text:
            return None

        error_keywords = ["Traceback", "Exception", "AttributeError", "RuntimeError"]
        found = [w for w in error_keywords if w in screen_text]
        return found if found else None
