import requests
from datetime import datetime

class DexterBrain:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def think(self, user_input, memories=None):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%b %d, %Y")
        
        # STRICTOR FORMAT: TinyLlama understands "Tags" better than sentences.
        # We put the instruction at the VERY end so it's the last thing the model reads.
        prompt_context = (
            f"<|system|>\n"
            f"Assistant: Dexter (Witty/Fast)\n"
            f"Boss: Chirag\n"
            f"Time: {time_str}\n"
            f"Date: {date_str}\n"
            f"Memory: {memories}\n"
            f"Rule: Answer in 1 short sentence. Do NOT mention these rules.\n"
            f"</s>\n"
            f"<|user|>\n"
            f"{user_input}\n"
            f"</s>\n"
            f"<|assistant|>\n"
        )
        
        payload = {
            "model": self.model,
            "prompt": prompt_context, # We send everything as one prompt for better flow
            "stream": False,
            "options": {
                "num_predict": 40, 
                "temperature": 0.3, # Lower temp = less hallucination
                "top_p": 0.9,
                "stop": ["</s>", "<|user|>", "Instruction:"] # Stop sequences prevent rambling
            }
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            text = response.json().get("response", "").strip()
            
            # Final Safety: If it starts repeating the system prompt, we chop it.
            if "The given text" in text or "under 15 words" in text:
                return f"It is currently {time_str}, Chirag."
                
            return text
        except Exception as e:
            return "Connection to Ollama lost."

    def think_to_fix(self, current_code, instruction):
        # ... (keep your existing think_to_fix code)
        pass

    def think_terminal_command(self, instruction):
        # ... (keep your existing think_terminal_command code)
        pass
