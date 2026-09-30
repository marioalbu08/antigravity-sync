# antigravity_sync/utils.py
import os
import sys
import shutil
import time
import subprocess
import json

def get_ide_db_path():
    """Finds the Antigravity IDE SQLite state database on any OS."""
    home = os.path.expanduser('~')
    if sys.platform == 'win32':
        p = os.path.join(home, 'AppData', 'Roaming', 'Antigravity IDE', 'User', 'globalStorage', 'state.vscdb')
    elif sys.platform == 'darwin':
        p = os.path.join(home, 'Library', 'Application Support', 'Antigravity IDE', 'User', 'globalStorage', 'state.vscdb')
    else:
        p = os.path.join(home, '.config', 'Antigravity IDE', 'User', 'globalStorage', 'state.vscdb')
    return p

def get_desktop_db_path():
    """Finds the Antigravity Desktop App SQLite state database on any OS."""
    home = os.path.expanduser('~')
    if sys.platform == 'win32':
        p = os.path.join(home, 'AppData', 'Roaming', 'Antigravity', 'User', 'globalStorage', 'state.vscdb')
    elif sys.platform == 'darwin':
        p = os.path.join(home, 'Library', 'Application Support', 'Antigravity', 'User', 'globalStorage', 'state.vscdb')
    else:
        p = os.path.join(home, '.config', 'Antigravity', 'User', 'globalStorage', 'state.vscdb')
    return p

def get_brain_dirs():
    """Returns a list of all Antigravity 'brain' directories to scan."""
    home = os.path.expanduser('~')
    dirs = [
        os.path.join(home, '.gemini', 'antigravity-ide', 'brain'),
        os.path.join(home, '.gemini', 'antigravity', 'brain')
    ]
    return [d for d in dirs if os.path.exists(d)]

def is_ide_running(check_desktop=False):
    """Checks if Antigravity IDE (or Desktop App) is currently running."""
    proc_name = "Antigravity.exe" if check_desktop else "Antigravity IDE.exe"
    proc_grep = "Antigravity" if check_desktop else "Antigravity IDE"
    
    try:
        if sys.platform == 'win32':
            output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {proc_name}"', shell=True, text=True)
            if proc_name in output:
                return True
        else:
            output = subprocess.check_output(f'pgrep -f "{proc_grep}"', shell=True, text=True)
            if output.strip():
                return True
    except Exception:
        pass
    return False

def wait_for_ide_close(check_desktop=False):
    """Blocks until Antigravity IDE (or Desktop App) is closed."""
    app_name = "Antigravity Desktop App" if check_desktop else "Antigravity IDE"
    if is_ide_running(check_desktop):
        print(f"{app_name} is currently running. Waiting for it to close...")
        while is_ide_running(check_desktop):
            time.sleep(2)
        print(f"{app_name} closed! Proceeding...")
        time.sleep(1) # Give SQLite a moment to release locks

def backup_db(db_path):
    """Creates a timestamped backup of the database."""
    if not os.path.exists(db_path):
        return None
    backup_path = db_path + f".backup_{int(time.time())}"
    shutil.copy2(db_path, backup_path)
    print(f"[Backup] Saved database to: {backup_path}")
    return backup_path

def clean_title(content):
    """Extracts a clean title from raw user input, stripping XML tags."""
    # Remove common XML tags
    for tag in ['<USER_REQUEST>', '</USER_REQUEST>', '<ADDITIONAL_METADATA>', '</ADDITIONAL_METADATA>']:
        content = content.replace(tag, '')
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if lines:
        title = lines[0]
        # Trim title nicely
        if len(title) > 60:
            title = title[:57] + '...'
        return title
    return "Restored Conversation"
