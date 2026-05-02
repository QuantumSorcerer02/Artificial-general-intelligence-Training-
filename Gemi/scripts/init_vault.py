import sqlite3
import os

def init_vault():
    vault_path = 'vault/astral_bloom_state.db'
    conn = sqlite3.connect(vault_path)
    cursor = conn.cursor()
    
    # Create table for the 416-space state-vaults
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS state_vaults (
            space_id INTEGER PRIMARY KEY,
            space_name TEXT,
            content TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create table for the 38,083 memories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            content TEXT,
            space_context INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Vault initialized at {vault_path}")

if __name__ == "__main__":
    init_vault()
