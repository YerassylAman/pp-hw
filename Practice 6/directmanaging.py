import os
import sys
from pathlib import Path

# Determine base directory: first argument if provided and not starting with '-'
if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
    base = Path(sys.argv[1])
    dir_names = sys.argv[2:]  # remaining args are directory names
else:
    base = Path.cwd()
    dir_names = sys.argv[1:]  # if no base, all args are dir names

# If no directory names given, read from stdin (e.g., from a file)
if not dir_names:
    dir_names = [line.strip() for line in sys.stdin if line.strip()]

if not dir_names:
    print("No directory names provided.")
    sys.exit(1)

for name in dir_names:
    target = base / name
    try:
        target.mkdir(parents=True, exist_ok=True)
        print(f"Created: {target}")
    except Exception as e:
        print(f"Failed to create {target}: {e}")


from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python move_files.py source_dir dest_dir [extensions...]")
    sys.exit(1)

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
extensions = sys.argv[3:]  # optional list of extensions (e.g., .txt .jpg)

if not src.is_dir():
    print(f"Source directory not found: {src}")
    sys.exit(1)

dst.mkdir(parents=True, exist_ok=True)

for item in src.iterdir():
    if not item.is_file():
        continue
    if extensions and item.suffix not in extensions:
        continue
    try:
        shutil.move(str(item), str(dst / item.name))
        print(f"Moved: {item.name}")
    except Exception as e:
        print(f"Error moving {item.name}: {e}")