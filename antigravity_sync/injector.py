# antigravity_sync/injector.py
import os
import sys
import uuid
import json
import time
from datetime import datetime, timezone

from .core import sync_conversations
from .utils import get_brain_dirs

def inject_markdown_conversation(md_path, db_path=None):
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
    
    # Smart markdown parser: detects conversation turns by common patterns
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common speaker markers used by ChatGPT, Claude, and manual exports
    import re
    turn_pattern = re.compile(
        r'^(?:\*\*|#{1,3}\s*)?(User|Human|You|Assistant|Claude|ChatGPT|AI|System|Model)[\s:*]*',
        re.IGNORECASE | re.MULTILINE
    )
    
    matches = list(turn_pattern.finditer(content))
    steps = []
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    if matches:
        # We found structured turns — parse them properly
        for i, match in enumerate(matches):
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            text = content[start:end].strip()
            
            speaker = match.group(1).lower()
            is_user = speaker in ('user', 'human', 'you')
            
            step = {
                "step_index": i,
                "source": "USER_EXPLICIT" if is_user else "MODEL",
                "type": "USER_INPUT" if is_user else "PLANNER_RESPONSE",
                "status": "DONE",
                "created_at": now,
                "content": f"<USER_REQUEST>\n{text}\n</USER_REQUEST>" if is_user else text
            }
            steps.append(step)
    else:
        # No structured turns found — fall back to treating it as a single exchange
        steps = [
            {
                "step_index": 0,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "status": "DONE",
                "created_at": now,
                "content": f"<USER_REQUEST>\n{title}\n</USER_REQUEST>"
            },
            {
                "step_index": 1,
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "status": "DONE",
                "created_at": now,
                "content": content
            }
        ]
    
    if not steps:
        print("Warning: No conversation content found in the file.")
        return
    
    print(f"  Detected {len(steps)} conversation turns.")
    print(f"Writing synthetic transcript to {transcript_path}")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        for step in steps:
            f.write(json.dumps(step) + '\n')
            
    print("Injection complete. Syncing database...")
    sync_conversations(db_path=db_path, dry_run=False)
    print(f"Success! Imported '{title}' as {cid}. Open Antigravity IDE to view it!")
