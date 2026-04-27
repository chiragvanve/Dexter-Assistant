import os
import sys
import webbrowser
import subprocess
import ctypes
import psutil
import time
import threading
from datetime import datetime
import re

# ── SHADOW DEPENDENCY MANAGEMENT ──────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
except ImportError:
    os.system(f"{sys.executable} -m pip install rich psutil requests -q")
    # Re-import after silent install

console = Console()
ACCENT = "#00FFB2" 

# ── THE DISPATCHER (Hands) ──────────────────────────────────────────────────
class DexterHands:
    def __init__(self):
        self.brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        self.registry = {
            "sekiro": "601150", "elden ring": "1245620",
            "code": "code", "notepad": "notepad.exe",
            "spotify": "spotify.exe", "discord": "discord.exe"
        }

    def dispatch(self, cmd: str):
        """God-Level Routing: Decides whether to use System, Web, or Logic."""
        # 1. Hardware/Telemetry Check
        if any(x in cmd for x in ["stats", "cpu", "ram", "battery"]):
            return self._get_telemetry()

        # 2. Game/App Registry
        for key, val in self.registry.items():
            if key in cmd:
                if val.isdigit():
                    webbrowser.open(f"steam://rungameid/{val}")
                    return f"◆ PROTOCOL: IGNITING {key.upper()}"
                os.system(f"start {val}")
                return f"◆ PROTOCOL: DEPLOYING {key.upper()}"

        # 3. Media & Web
        if "play" in cmd or "youtube" in cmd:
            query = re.sub(r'play|on|youtube', '', cmd).strip().replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"◆ STREAMING: {query.replace('+', ' ').upper()}"

        # 4. System Lockdown
        if "lock" in cmd:
            ctypes.windll.user32.LockWorkStation()
            return "◆ SECURITY: WORKSTATION ENCRYPTED."

        return None # Pass to LLM Brain if no hard match

    def _get_telemetry(self):
        # Returns raw data for the TUI to format
        batt = psutil.sensors_battery()
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "bat": batt.percent if batt else 0
        }

# ── THE CORE ENGINE ──────────────────────────────────────────────────────────
class DexterCore:
    def __init__(self):
        self.hands = DexterHands()
        self.boot_time = datetime.now()
        self.session_log = []

    def process_input(self, raw_input: str):
        if not raw_input.strip(): return None
        
        # Immediate Terminal Passthrough
        if raw_input.startswith(("$", ">")):
            cmd = raw_input[1:].strip()
            subprocess.Popen(f"cmd /c {cmd}", shell=True)
            return f"EXECUTING SHELL: {cmd}"

        # Try Physical Dispatch
        response = self.hands.dispatch(raw_input.lower())
        
        # If Hands don't know, suggest a Google fallback (Logic layer integration)
        if not response:
            webbrowser.open(f"https://www.google.com/search?q={raw_input.replace(' ', '+')}")
            response = f"INTENT UNKNOWN. DEPLOYING SEARCH: {raw_input.upper()}"
            
        self.session_log.append((datetime.now().strftime("%H:%M"), raw_input, response))
        return response

# ── GOD LEVEL TUI COMPONENTS ──────────────────────────────────────────────────
def get_stats_table(hands):
    data = hands._get_telemetry()
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Label", style="dim")
    table.add_column("Value", style=f"bold {ACCENT}")
    
    table.add_row("CPU", f"{data['cpu']}%")
    table.add_row("RAM", f"{data['ram']}%")
    table.add_row("BAT", f"{data['bat']}%")
    return table

def boot_sequence():
    console.clear()
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold white]{task.description}"),
        BarColumn(bar_width=40, pulse_style=ACCENT),
        console=console
    ) as progress:
        t1 = progress.add_task("Initializing Dexter Core...", total=100)
        t2 = progress.add_task("Calibrating Hardware Hands...", total=100)
        while not progress.finished:
            progress.update(t1, advance=random.uniform(1, 5))
            progress.update(t2, advance=random.uniform(1, 3))
            time.sleep(0.05)

# ── MAIN EXECUTION ────────────────────────────────────────────────────────────
def run_dexter():
    core = DexterCore()
    boot_sequence()
    
    console.clear()
    console.print(Panel(Align.center(f"[bold {ACCENT}]DEXTER SYSTEM V2 // PUNE SECTOR[/bold {ACCENT}]"), border_style=ACCENT))

    while True:
        # Side-car Stats Display
        stats = get_stats_table(core.hands)
        console.print(Columns([stats, Panel(f"[dim]UPTIME:[/dim] [bold]{datetime.now()-core_boot:}[/bold]", border_style="#333333")], width=30))
        
        user_in = Prompt.ask(f"\n[bold {ACCENT}]▶ COMMAND[/bold {ACCENT}]")
        
        if user_in.lower() in ["exit", "quit"]:
            console.print(f"[bold red]SHUTTING DOWN SYSTEM...[/bold red]")
            break
            
        response = core.process_input(user_in)
        if response:
            console.print(Panel(Text(response, style=f"bold {ACCENT}"), border_style=ACCENT, title="[dim]DEXTER_RESPONSE[/dim]"))

if __name__ == "__main__":
    core_boot = datetime.now()
    run_dexter()
