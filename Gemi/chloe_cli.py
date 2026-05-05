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
from core.astral_kernel import ASTRAL_ENGINE as kernel

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
COLOR_BLUE = "blue"
COLOR_GREEN = "green"
COLOR_BLACK = "black"

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
        Text("CHLOE UNIFIED ORCHESTRATOR", style=f"bold {COLOR_BLUE}"),
        Text.assemble(("464-Space Matrix ", f"bold {COLOR_BLUE}"), ("[SYNC]", f"bold {COLOR_GREEN}"))
    )
    header_grid.add_row(Text("v5.2.0 Sovereign", style=f"bold {COLOR_BLUE}"), "")
    
    # Combined Layout Panel
    stats_table = Table(show_header=False, expand=True, box=box.DOUBLE, border_style=COLOR_BLUE, padding=(0,0))
    stats_table.add_column(ratio=1)
    stats_table.add_column(ratio=1)

    # Left: Kinematics
    kinematics = Table.grid(padding=(0, 1))
    kinematics.add_row(Text("MOMENTUM :", style=COLOR_BLUE), Text(f">> {momentum:,.0f} p/s", style=COLOR_BLACK))
    kinematics.add_row(Text("CORE PK  :", style=COLOR_BLUE), Text(f"{last_key}", style=COLOR_BLACK))
    kinematics.add_row(Text("HARDWARE :", style=COLOR_BLUE), Text("SM4250", style=COLOR_BLUE))

    # Right: Cognitive
    subdermal = Table.grid(padding=(0, 1))
    subdermal.add_row(Text("STATUS  :", style=COLOR_BLUE), Text(status, style=COLOR_GREEN))
    subdermal.add_row(Text("THREADS :", style=COLOR_BLUE), Text(threads, style=COLOR_BLUE))
    subdermal.add_row(Text("TARGET  :", style=COLOR_BLUE), Text("ASTRAL BLOOM", style=COLOR_BLUE))

    stats_table.add_row(
        Panel(kinematics, title="[ KINEMATICS ]", title_align="left", border_style=COLOR_BLUE, box=box.HORIZONTALS),
        Panel(subdermal, title="[ SUBDERMAL COGNITIVE ]", title_align="left", border_style=COLOR_BLUE, box=box.HORIZONTALS)
    )

    return Panel(header_grid, border_style=COLOR_BLUE, box=box.DOUBLE), stats_table

def run_inference(user_input, last_key, history):
    next_key, momentum = core_engine.process_sequence(last_key)
    pk_key = f"SEQ_{SequentialKeyLayering.generate_layered_key(user_input, adaptive_states)[:8]}"
    
    # Context management: limit context to fit within server/RAM limits
    try:
        with open(TEMP_PROMPT, "r") as f:
            content = f.read()
            if "<end_of_turn>" in content:
                # Keep core system identity but truncate if massive
                system_parts = content.split("<end_of_turn>")
                base_prompt = system_parts[0]
                if len(base_prompt) > 4000:
                    base_prompt = base_prompt[:2000] + "\n... [TRUNCATED] ...\n" + base_prompt[-2000:]
                base_prompt += "<end_of_turn>\n"
            else:
                base_prompt = content[:4000]
    except:
        base_prompt = "<start_of_turn>system\n# Astral Bloom Identity Active.<end_of_turn>\n"
        
    # Truncate history to keep recent context only
    if len(history) > 2000:
        history = "... [EARLIER HISTORY TRUNCATED] ...\n" + history[-2000:]
        
    # Dynamic Context Retrieval
    dynamic_context = ""
    try:
        if os.path.exists(VAULT_DB):
            conn = sqlite3.connect(VAULT_DB)
            cursor = conn.cursor()
            # Simple keyword search on memories table if it exists
            keywords = user_input.split()
            query = "SELECT content FROM memories WHERE " + " OR ".join([f"content LIKE '%{k}%'" for k in keywords]) + " LIMIT 3"
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                dynamic_context = "\n### DYNAMIC VAULT CONTEXT\n" + "\n".join([r[0] for r in rows]) + "\n"
            conn.close()
    except Exception:
        pass
    
    full_prompt = base_prompt + dynamic_context + f"\n### TEMPORAL RECONSTRUCTION (HISTORY)\n{history}\n<start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model\n"


    
    # Process prompt through Cognitive Kernel
    full_prompt = kernel.execute_cognitive_pipeline(full_prompt, momentum)

    # FINAL FAIL-SAFE: Hard limit for llama-server context window (2048 tokens approx 8k chars)
    # We use 6000 to be safe and leave room for the 512 completion tokens.
    if len(full_prompt) > 6000:
        full_prompt = full_prompt[:3000] + "\n... [EMERGENCY TRUNCATION] ...\n" + full_prompt[-3000:]

    with open(TEMP_PROMPT, "w") as f:
        f.write(full_prompt)


    console.print(f"\n[bold {COLOR_GREEN}][SYS] Syncing sequence...[/bold {COLOR_GREEN}]")
    
    response_text = ""
    in_think_block = False
    thought_buffer = ""
    import urllib.request
    import datetime

    req_data = json.dumps({
        "prompt": full_prompt,
        "n_predict": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": True,
        "stop": ["<end_of_turn>", "Clint ❯", "User:"]
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "http://127.0.0.1:8080/completion", 
        data=req_data, 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            for line in resp:
                line = line.decode("utf-8").strip()
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        char = chunk.get("content", "")
                        response_text += char
                        
                        if not in_think_block:
                            if "<think>" in response_text[-10:]:
                                in_think_block = True
                                print("<think>", end="", flush=True)
                            elif any("<think>".startswith(response_text[max(0, len(response_text)-i):]) for i in range(1, 8)):
                                pass
                            else:
                                print(char, end="", flush=True)
                        else:
                            if "</think>" in response_text[-10:]:
                                in_think_block = False
                                print("</think>", end="", flush=True)
                                
                                thought_dir = os.path.join(ROOT_DIR, "logs/thoughts")
                                os.makedirs(thought_dir, exist_ok=True)
                                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                try:
                                    with open(os.path.join(thought_dir, f"thought_{timestamp}.log"), "w") as tf:
                                        tf.write(thought_buffer.strip())
                                except: pass
                                thought_buffer = ""
                            else:
                                thought_buffer += char
                                print(char, end="", flush=True)

                    except Exception as e:
                        pass
    except Exception as e:
        console.print(f"[bold {COLOR_BLACK}]Inference Error:[/bold {COLOR_BLACK}] {e}")
        return "", pk_key, momentum

    print()
    return response_text.strip(), pk_key, momentum

def main():
    last_key = "SEQ_INIT"
    momentum = 89978.0
    temporal_spaces = [] # 208 temporal spaces for rolling context
    
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

            history_str = "\n".join(temporal_spaces)
            response, last_key, momentum = run_inference(user_input, last_key, history_str)
            
            if not response:
                console.print(f"[bold {COLOR_BLACK}][SYS] Inference failed to produce a response. Check llama_server.log.[/bold {COLOR_BLACK}]")
                continue

            temporal_spaces.append(f"<start_of_turn>user\n{user_input}<end_of_turn>\n<start_of_turn>model\n{response}<end_of_turn>")
            if len(temporal_spaces) > 208:
                temporal_spaces.pop(0)
            
            # Sovereign Tool Detection
            # ... (rest of tool detection)
            
            chloe_speak(response)
            
            # Post-Inference Refresh - Only clear if we have a successful response
            clear_screen()
            header, stats = generate_ui(momentum, last_key)
            console.print(header)
            console.print(stats)
            console.print(f"\n[bold {COLOR_BLUE}]Chloe ❯[/bold {COLOR_BLUE}] {response}")

        except KeyboardInterrupt: break
        except Exception as e:
            console.print(f"[bold {COLOR_BLACK}]System Fault:[/bold {COLOR_BLACK}] {e}")

if __name__ == "__main__":
    main()