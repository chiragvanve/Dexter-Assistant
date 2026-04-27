import tkinter as tk
from tkinter import font as tkfont
import sys

class SentinelIsland:
    def __init__(self, main_instance=None):
        self.root = tk.Tk()
        self.root.title("DEXTER_HUD_FROSTED")
        
        self.dexter_main = main_instance 
        self.external_trigger = None 
        self.external_text_trigger = None 
        
        # --- COLOR PALETTE ---
        self.invisible_key = "#000001" 
        self.bg_color = "#ffffff"     
        self.text_color = "#1a1a1a"   
        self.accent_color = "#0078D7" 
        self.hover_color = "#3399FF" # Lighter blue for hover state
        
        # --- WINDOW SETUP ---
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True) 
        self.root.attributes("-alpha", 0.75) # 75% Opaque (Frosted Glass)
        self.root.wm_attributes("-transparentcolor", self.invisible_key)
        self.root.config(bg=self.invisible_key)
        
        # --- ADJUSTED DIMENSIONS ---
        screen_w = self.root.winfo_screenwidth()
        self.width, self.height = 700, 140 
        self.root.geometry(f"{self.width}x{self.height}+{int(screen_w/2 - 350)}+20")

        self.main_font = tkfont.Font(family="Segoe UI Variable Display", size=13, weight="bold")
        self.sub_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        
        self.canvas = tk.Canvas(self.root, bg=self.invisible_key, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw the Frosted UI
        self.bg_rect = self.round_rectangle(10, 10, self.width-10, self.height-10, radius=35, fill=self.bg_color)
        self.core = self.canvas.create_oval(30, 45, 45, 60, fill=self.accent_color, outline="")
        
        self.sys_text = self.canvas.create_text(60, 25, text="DEXTER // STANDBY", fill="#888888", font=self.sub_font, anchor="nw")
        
        # --- ADJUSTED LABEL WRAPLENGTH ---
        self.label = tk.Label(self.root, text="INITIALIZING...", fg=self.text_color, bg=self.bg_color, font=self.main_font, wraplength=600, justify="left")
        self.label_window = self.canvas.create_window(60, 45, anchor="nw", window=self.label)

        # --- THE COMMAND ENTRY BOX ---
        self.cmd_var = tk.StringVar()
        self.cmd_entry = tk.Entry(self.root, textvariable=self.cmd_var, font=self.main_font, bg="#f0f0f0", fg=self.accent_color, bd=0, highlightthickness=0, insertbackground=self.text_color)
        self.cmd_entry.bind("<Return>", self.submit_text) 
        self.cmd_entry.bind("<Escape>", self.cancel_typing) # Hit Esc to hide box
        self.entry_window = self.canvas.create_window(60, 75, anchor="nw", window=self.cmd_entry, width=520, state="hidden")

        # --- CONTEXT MENU (Right Click) ---
        self.menu = tk.Menu(self.root, tearoff=0, bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 10), bd=0, activebackground="#e0e0e0", activeforeground=self.text_color)
        self.menu.add_command(label="⌨️ Type Command", command=self.enable_typing)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Shutdown Dexter", command=self.shutdown_system)

        # --- INTERACTIVE BINDINGS ---
        # 1. Hover Physics
        self.root.bind("<Enter>", self.on_hover_enter)
        self.root.bind("<Leave>", self.on_hover_leave)
        
        # 2. Click to Talk (Left Click)
        self.canvas.tag_bind(self.bg_rect, "<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        
        # 3. Double-Click to Type
        self.canvas.tag_bind(self.bg_rect, "<Double-Button-1>", lambda e: self.enable_typing())
        self.label.bind("<Double-Button-1>", lambda e: self.enable_typing())
        
        # 4. Context Menu (Right Click)
        self.root.bind("<Button-3>", self.show_context_menu)
        
        # 5. Drag the Window (Shift + Left Click)
        self.root.bind("<Shift-Button-1>", self.start_move)
        self.root.bind("<Shift-B1-Motion>", self.do_move)

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, outline="", smooth=True)

    # --- INTERACTION LOGIC ---
    def on_hover_enter(self, event):
        """Highlights the core when the mouse hovers over the HUD."""
        if self.canvas.itemcget(self.sys_text, 'text') == "DEXTER // STANDBY":
            self.canvas.itemconfig(self.core, fill=self.hover_color)

    def on_hover_leave(self, event):
        """Returns the core to normal when the mouse leaves."""
        if self.canvas.itemcget(self.sys_text, 'text') == "DEXTER // STANDBY":
            self.canvas.itemconfig(self.core, fill=self.accent_color)

    def show_context_menu(self, event):
        """Pops up the Right-Click menu."""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def shutdown_system(self):
        """Safely kills the application."""
        self.trigger_pop("SYSTEM OFFLINE", duration=0)
        self.root.update()
        sys.exit(0)

    def on_click(self, event):
        if self.external_trigger:
            self.external_trigger(voice_mode=True)

    def enable_typing(self):
        self.canvas.itemconfigure(self.entry_window, state="normal")
        self.cmd_entry.focus_set()
        self.trigger_pop("AWAITING KEYBOARD INPUT...", duration=0)

    def cancel_typing(self, event):
        """Hides the text box if you press Esc."""
        self.cmd_var.set("")
        self.canvas.itemconfigure(self.entry_window, state="hidden")
        self.root.focus_set()
        self.trigger_pop("READY", duration=0)

    def submit_text(self, event):
        command = self.cmd_var.get().strip()
        self.cmd_var.set("") 
        self.canvas.itemconfigure(self.entry_window, state="hidden") 
        self.root.focus_set() 
        
        if command and self.external_text_trigger:
            self.external_text_trigger(text_input=command)

    def update_status(self, status_text, is_active=False):
        self.canvas.itemconfig(self.sys_text, text=f"DEXTER // {status_text.upper()}")
        if is_active:
            self.canvas.itemconfig(self.core, fill="#00FFB2")
        else:
            self.canvas.itemconfig(self.core, fill=self.accent_color)

    def trigger_pop(self, text, duration=3000):
        self.label.config(text=text.upper())
        if duration > 0:
            self.root.after(duration, lambda: self.label.config(text="READY"))

    def start_move(self, event):
        self.x, self.y = event.x, event.y
        
    def do_move(self, event):
        self.root.geometry(f"+{self.root.winfo_x() + (event.x - self.x)}+{self.root.winfo_y() + (event.y - self.y)}")
        
    def loop(self):
        self.root.mainloop()
