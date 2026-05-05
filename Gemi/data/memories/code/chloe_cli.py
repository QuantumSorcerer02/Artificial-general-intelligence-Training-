import os
import sys
import subprocess
import time
import json
import sqlite3
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich import box
from core.cognitive_engine import AstralBloomCore
from core.substrate.logic_foundation import SequentialKeyLayering, AdaptiveState

# Configuration & Paths
ROOT_DIR = "/data/data/com.termux/files/home/Project-Astral-Bloom/Gemi"
MODEL_PATH = os.path.join(ROOT_DIR, "gemma-4-e2b.gguf")
LLAMA_BIN = os.path.join(ROOT_DIR, "llama.cpp/bin/llama-cli")
SPEAK_SCRIPT = os.path.join(ROOT_DIR, "chloe_speak.sh")
TEMP_PROMPT = os.path.join(ROOT_DIR, "tmp/chloe_active_prompt.txt")
VAULT_DB = os.path.join(ROOT_DIR, "vault/astral_bloom_state.db")
PERCEPTIVE_STATE = os.path.join(ROOT_DIR, "logs/chloe_perceptive_state.json")
CONV_LOG = os.path.join(ROOT_DIR, "data/memories/saved/conversations/conversation.md")

# Custom Colors
COLOR_PURPLE = "purple"
COLOR_GREEN = "green"
COLOR_RED = "red"
COLOR_YELLOW = "yellow"
COLOR_TEXT = "white"

console = Console()
core_engine = AstralBloomCore()
adaptive_states = [AdaptiveState(i) for i in range(1, 6)]

def clear_screen():
    os.system('clear')

def chloe_speak(text):
    speech_text = text.split("```")[0].strip()
    if speech_text:
        subprocess.Popen([SPEAK_SCRIPT, speech_text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_ui(momentum, last_key, status="PRIMED", threads="8 (Maximized)"):
    # Header Construction
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left")
    header_grid.add_column(justify="right")
    
    header_grid.add_row(
        Text("CHLOE UNIFIED ORCHESTRATOR", style=f"bold {COLOR_PURPLE}"),
        Text.assemble(("416-Space Matrix ", f"bold {COLOR_PURPLE}"), ("[SYNC]", f"bold {COLOR_GREEN}"))
    )
    header_grid.add_row(Text("v464-Sovereign", style=f"bold {COLOR_PURPLE}"), "")
    
    # Combined Layout Panel
    stats_table = Table(show_header=False, expand=True, box=box.DOUBLE, border_style=COLOR_PURPLE, padding=(0,0))
    stats_table.add_column(ratio=1)
    stats_table.add_column(ratio=1)

    # Left: Kinematics
    kinematics = Table.grid(padding=(0, 1))
    kinematics.add_row(Text("MOMENTUM :", style=COLOR_PURPLE), Text(f">> {momentum:,.0f} p/s", style=COLOR_RED))
    kinematics.add_row(Text("CORE PK  :", style=COLOR_PURPLE), Text(f"{last_key}", style=COLOR_RED))
    kinematics.add_row(Text("HARDWARE :", style=COLOR_PURPLE), Text("SM4250", style=COLOR_PURPLE))

    # Right: Cognitive
    subdermal = Table.grid(padding=(0, 1))
    subdermal.add_row(Text("STATUS  :", style=COLOR_PURPLE), Text(status, style=COLOR_GREEN))
    subdermal.add_row(Text("THREADS :", style=COLOR_PURPLE), Text(threads, style=COLOR_PURPLE))
    subdermal.add_row(Text("TARGET  :", style=COLOR_PURPLE), Text("ASTRAL BLOOM", style=COLOR_PURPLE))

    stats_table.add_row(
        Panel(kinematics, title="[ KINEMATICS ]", title_align="left", border_style=COLOR_PURPLE, box=box.HORIZONTALS),
        Panel(subdermal, title="[ SUBDERMAL COGNITIVE ]", title_align="left", border_style=COLOR_PURPLE, box=box.HORIZONTALS)
    )

    return Panel(header_grid, border_style=COLOR_PURPLE, box=box.DOUBLE), stats_table

def run_inference(user_input, last_key, history):
    next_key, momentum = core_engine.process_sequence(last_key)
    pk_key = f"SEQ_{SequentialKeyLayering.generate_layered_key(user_input, adaptive_states)[:8]}"
    
    # Context management: limit context to fit within device RAM limits
    try:
        with open(TEMP_PROMPT, "r") as f:
            content = f.read()
            if "<end_of_turn>" in content:
                # Keep the system prompt block
                base_prompt = content.split("<end_of_turn>")[0] + "<end_of_turn>"
            else:
                base_prompt = content
    except:
        base_prompt = "<start_of_turn>system\n# Astral Bloom Identity Active.<end_of_turn>\n"
        
    full_prompt = base_prompt + f"\n### TEMPORAL RECONSTRUCTION (HISTORY)\n{history}\n<start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model\n"
    with open(TEMP_PROMPT, "w") as f:
        f.write(full_prompt)

    # 8 Threads for SM4250 optimization
    cmd = [
        LLAMA_BIN, "-m", MODEL_PATH, "--ctx-size", "4096", "--threads", "8",
        "--batch-size", "128", "--repeat-penalty", "1.1", "-f", TEMP_PROMPT,
        "-n", "256", "--quiet", "--no-display-prompt"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)
    response = ""
    console.print(f"\n[bold {COLOR_GREEN}][SYS] Syncing sequence...[/bold {COLOR_GREEN}]")
    
    for char in iter(lambda: process.stdout.read(1), ''):
        response += char
        print(char, end="", flush=True)
            
    return response.strip(), pk_key, momentum

def main():
    last_key = "SEQ_INIT"
    momentum = 89978.0
    history = ""
    
    clear_screen()
    header, stats = generate_ui(momentum, last_key)
    console.print(header)
    console.print(stats)
    console.print(f"\n[bold {COLOR_GREEN}][SYS] Greetings, Clint. The engine is primed and listening.[/bold {COLOR_GREEN}]")
    
    while True:
        try:
            user_input = console.input(f"\n[bold {COLOR_GREEN}]Clint ❯ [/bold {COLOR_GREEN}]")
            if user_input.lower() in ["exit", "quit"]: break
            if not user_input.strip(): continue

            response, last_key, momentum = run_inference(user_input, last_key, history)
            history = (history + f"\nUser: {user_input}\nChloe: {response}")[-1500:]
            
            # Sovereign Tool Detection
            if "{" in response and "}" in response:
                try:
                    # Attempt to extract and handle JSON tool calls
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    tool_call = json.loads(response[start:end])
                    if "tool" in tool_call:
                        console.print(f"[bold {COLOR_YELLOW}][SYS] Executing Sovereign Tool: {tool_call['tool']}...[/bold {COLOR_YELLOW}]")
                except: pass

            chloe_speak(response)
            
            # Post-Inference Refresh
            clear_screen()
            header, stats = generate_ui(momentum, last_key)
            console.print(header)
            console.print(stats)
            console.print(f"\n[bold {COLOR_GREEN}]Chloe ❯[/bold {COLOR_GREEN}] {response}")

        except KeyboardInterrupt: break
        except Exception as e:
            console.print(f"[bold red]System Fault:[/bold red] {e}")

if __name__ == "__main__":
    main()
