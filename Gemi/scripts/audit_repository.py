import os
import ast
import re

ROOT_DIR = "."
OUTDATED_PATTERNS = [r'\b416-Space\b', r'\bNUM_SPACES\s*=\s*416\b', r'\b48 Aux\b', r'\b208 Core\b']
EXCLUDE_DIRS = ['node_modules', '.git', '__pycache__', 'tmp', 'venv', '.gemini']

results = {"syntax_errors": [], "outdated_refs": [], "total_files": 0, "py_files": 0, "md_files": 0}

for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for file in filenames:
        results["total_files"] += 1
        filepath = os.path.join(dirpath, file)
        
        if file.endswith('.py'):
            results["py_files"] += 1
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    ast.parse(content)
                    
                    for i, line in enumerate(content.split('\n')):
                        for pattern in OUTDATED_PATTERNS:
                            if re.search(pattern, line):
                                results["outdated_refs"].append(f"{filepath}:{i+1} - {line.strip()}")
            except SyntaxError as e:
                results["syntax_errors"].append(f"{filepath}: {e}")
            except Exception:
                pass
                
        elif file.endswith('.md'):
            results["md_files"] += 1
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for i, line in enumerate(content.split('\n')):
                        for pattern in OUTDATED_PATTERNS:
                            if re.search(pattern, line):
                                results["outdated_refs"].append(f"{filepath}:{i+1} - {line.strip()}")
            except Exception:
                pass

print(f"--- ASTRAL BLOOM AUDIT REPORT ---")
print(f"Total Files Scanned: {results['total_files']}")
print(f"Python Files: {results['py_files']}")
print(f"Markdown Files: {results['md_files']}")
print(f"\n--- SYNTAX ERRORS ({len(results['syntax_errors'])}) ---")
for err in results["syntax_errors"]: print(err)
print(f"\n--- OUTDATED ARCHITECTURE REFERENCES ({len(results['outdated_refs'])}) ---")
for ref in results["outdated_refs"][:20]: print(ref)
if len(results["outdated_refs"]) > 20: print(f"...and {len(results['outdated_refs']) - 20} more.")
