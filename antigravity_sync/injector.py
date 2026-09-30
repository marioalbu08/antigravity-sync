# antigravity_sync/injector.py
import os
import sys
import uuid
import json
import time
from datetime import datetime, timezone

from .core import sync_conversations
from .utils import get_brain_dirs

def inject_markdown_conversation(md_path):
    """
    Parses a simple markdown file (e.g. from ChatGPT or Claude) and creates a 
    synthetic Antigravity transcript, then automatically syncs it into the IDE.
    """
    if not os.path.exists(md_path):
        print(f"Error: Could not find file {md_path}")
        return
        
    title = os.path.basename(md_path).replace('.md', '')
    cid = str(uuid.uuid4())
    
    # Locate IDE brain dir
    brain_dirs = [d for d in get_brain_dirs() if 'antigravity-ide' in d]
    if not brain_dirs:
        home = os.path.expanduser('~')
        ide_brain = os.path.join(home, '.gemini', 'antigravity-ide', 'brain')
        os.makedirs(ide_brain, exist_ok=True)
    else:
        ide_brain = brain_dirs[0]
        
    target_dir = os.path.join(ide_brain, cid, '.system_generated', 'logs')
    os.makedirs(target_dir, exist_ok=True)
    
    transcript_path = os.path.join(target_dir, 'transcript.jsonl')
    
    print(f"Parsing {md_path}...")
    
    # Super basic MD parser: treats alternating sections as User/Model
    # In a real app, you might look for "**User:**" or similar headings.
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We will just split by a common heuristic or chunk it.
    # For now, if there is no explicit parsing, we just inject it as one big user request + model response
    # to guarantee it works.
    steps = []
    
    # Dummy user step
    user_step = {
        "step_index": 0,
        "source": "USER_EXPLICIT",
        "type": "USER_INPUT",
        "status": "DONE",
        "created_at": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "content": f"<USER_REQUEST>\n{title}\n</USER_REQUEST>"
    }
    steps.append(user_step)
    
    # Model response step
    model_step = {
        "step_index": 1,
        "source": "MODEL",
        "type": "PLANNER_RESPONSE",
        "status": "DONE",
        "created_at": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "content": content
    }
    steps.append(model_step)
    
    print(f"Writing synthetic transcript to {transcript_path}")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        for step in steps:
            f.write(json.dumps(step) + '\n')
            
    print("Injection complete. Syncing database...")
    sync_conversations(dry_run=False)
    print(f"Success! Imported '{title}' as {cid}. Open Antigravity IDE to view it!")
