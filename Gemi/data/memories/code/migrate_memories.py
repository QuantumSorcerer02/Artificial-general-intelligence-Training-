import sqlite3
import os
import sys

def migrate_memories():
    # Base directory is one level up from scripts
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vault_path = os.path.join(base_dir, 'vault', 'astral_bloom_state.db')
    memories_dir = os.path.join(base_dir, 'data', 'memories')
    
    if not os.path.exists(vault_path):
        print(f"Vault not found at {vault_path}. Please initialize the vault first.")
        sys.exit(1)

    conn = sqlite3.connect(vault_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memories';")
    if not cursor.fetchone():
        print("Table 'memories' not found. Ensure init_vault.py has been run.")
        sys.exit(1)
    
    # Optional: Clear existing records before migrating
    cursor.execute("DELETE FROM memories;")
    conn.commit()

    count = 0
    errors = 0
    
    for root, dirs, files in os.walk(memories_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, memories_dir)
            
            try:
                # Try to read text content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                space_context = 0  # Default space context
                
                cursor.execute('''
                    INSERT INTO memories (source_file, content, space_context)
                    VALUES (?, ?, ?)
                ''', (rel_path, content, space_context))
                
                count += 1
                
                if count % 1000 == 0:
                    conn.commit()
                    print(f"Migrated {count} records...")
                    
            except UnicodeDecodeError:
                # Likely binary or non-utf-8, skip
                errors += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                errors += 1
                
    conn.commit()
    conn.close()
    
    print(f"Migration complete. Inserted {count} records successfully. Encountered {errors} unreadable/binary files.")

if __name__ == "__main__":
    print("[ASTRAL BLOOM] Initiating Data Factory Migration to SQLite...")
    migrate_memories()