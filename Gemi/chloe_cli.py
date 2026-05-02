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
from core.cognitive_kernel import FORMULA_ENGINE

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
        Text.assemble(("416-Space Matrix ", f"bold {COLOR_BLUE}"), ("[SYNC]", f"bold {COLOR_GREEN}"))
    )
    header_grid.add_row(Text("v464-Sovereign", style=f"bold {COLOR_BLUE}"), "")
    
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
    full_prompt = FORMULA_ENGINE.execute_cognitive_pipeline(full_prompt, momentum)

    with open(TEMP_PROMPT, "w") as f:
        f.write(full_prompt)

    # 8 Threads for SM4250 optimization
    cmd = [
        LLAMA_BIN, "-m", MODEL_PATH, "--ctx-size", "0", "--threads", "8",
        "--batch-size", "128", "--repeat-penalty", "1.1", "-f", TEMP_PROMPT,
        "-n", "-1", "--log-disable", "--no-display-prompt"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1)
    response = ""
    console.print(f"\n[bold {COLOR_GREEN}][SYS] Syncing sequence...[/bold {COLOR_GREEN}]")
    
    in_think_block = False
    thought_buffer = ""
    buffer = ""
    import datetime
    
    for char in iter(lambda: process.stdout.read(1), ''):
        response += char
        buffer += char
        
        if not in_think_block:
            if "<think>" in buffer:
                in_think_block = True
                pre_think = buffer.split("<think>")[0]
                if pre_think:
                    print(pre_think, end="", flush=True)
                buffer = ""
                thought_buffer = ""
            elif any("<think>".startswith(buffer[i:]) for i in range(len(buffer))):
                pass
            else:
                print(buffer, end="", flush=True)
                buffer = ""
        else:
            if "</think>" in buffer:
                in_think_block = False
                thought_buffer += buffer.split("</think>")[0]
                buffer = buffer.split("</think>")[1]
                
                thought_dir = os.path.join(ROOT_DIR, "logs/thoughts")
                os.makedirs(thought_dir, exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                try:
                    with open(os.path.join(thought_dir, f"thought_{timestamp}.log"), "w") as tf:
                        tf.write(thought_buffer.strip())
                except: pass
                
                thought_buffer = ""
            elif any("</think>".startswith(buffer[i:]) for i in range(len(buffer))):
                pass
            else:
                thought_buffer += buffer
                buffer = ""

    if buffer and not in_think_block:
        print(buffer, end="", flush=True)
            
    return response.strip(), pk_key, momentum

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
            
            temporal_spaces.append(f"User: {user_input}\nChloe: {response}")
            if len(temporal_spaces) > 208:
                temporal_spaces.pop(0)
            
            # Sovereign Tool Detection
            if "{" in response and "}" in response:
                try:
                    # Attempt to extract and handle JSON tool calls
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    tool_call = json.loads(response[start:end])
                    tool_name = tool_call.get("tool") or tool_call.get("command")
                    if tool_name:
                        console.print(f"[bold {COLOR_GREEN}][SYS] Executing Sovereign Tool: {tool_name}...[/bold {COLOR_GREEN}]")
                        
                        args = tool_call.get("args", "")
                        cmd_to_run = tool_name
                        if isinstance(args, dict):
                            for k, v in args.items():
                                cmd_to_run += f" --{k} '{v}'"
                        elif isinstance(args, list):
                            cmd_to_run += " " + " ".join(str(a) for a in args)
                        elif isinstance(args, str) and args:
                            cmd_to_run += f" {args}"
                            
                        try:
                            result = subprocess.run(cmd_to_run, shell=True, capture_output=True, text=True, timeout=60)
                            tool_output = (result.stdout + result.stderr).strip()
                            if not tool_output:
                                tool_output = f"Executed {tool_name} successfully."
                            
                            temporal_spaces.append(f"[Tool Result]: {tool_output}")
                            if len(temporal_spaces) > 208: temporal_spaces.pop(0)
                            
                            console.print(f"[bold {COLOR_GREEN}][SYS] Tool execution complete.[/bold {COLOR_GREEN}]")
                        except Exception as e:
                            temporal_spaces.append(f"[Tool Error]: {str(e)}")
                            if len(temporal_spaces) > 208: temporal_spaces.pop(0)
                            
                            console.print(f"[bold {COLOR_BLACK}][SYS] Tool execution failed: {e}[/bold {COLOR_BLACK}]")
                except: pass

            chloe_speak(response)
            
            # Post-Inference Refresh
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