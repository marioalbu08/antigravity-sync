# antigravity_sync/core.py
import os
import json
import sqlite3
import base64
import blackboxprotobuf
from datetime import datetime

from .schema import TOP_TYPEDEF, INNER_TYPEDEF, create_inner_msg
from .utils import backup_db, get_ide_db_path, get_brain_dirs

def parse_transcript_metadata(t_path):
    """Reads a transcript.jsonl file and extracts title, timestamps, and step count."""
    title = "Restored Conversation"
    created_ts = int(os.path.getctime(t_path))
    updated_ts = int(os.path.getmtime(t_path))
    step_count = 0
    
    try:
        with open(t_path, 'r', encoding='utf-8') as f:
            for line in f:
                step = json.loads(line)
                step_count += 1
                
                # Try to parse timestamp from first step
                if step_count == 1 and 'created_at' in step:
                    try:
                        # e.g., 2024-10-30T10:25:58Z or 2024-10-30T10:25:58.123Z
                        clean_ts = step['created_at'].replace('Z', '').split('.')[0]
                        dt = datetime.strptime(clean_ts, '%Y-%m-%dT%H:%M:%S')
                        created_ts = int(dt.timestamp())
                    except Exception:
                        pass
                        
                # Get title from first user request
                if title == "Restored Conversation" and (step.get('source') == 'USER_EXPLICIT' or step.get('type') == 'USER_INPUT'):
                    from .utils import clean_title
                    title = clean_title(step.get('content', ''))
                    
            # Use last step's timestamp if available
            if 'created_at' in step:
                try:
                    clean_ts = step['created_at'].replace('Z', '').split('.')[0]
                    dt = datetime.strptime(clean_ts, '%Y-%m-%dT%H:%M:%S')
                    updated_ts = int(dt.timestamp())
                except Exception:
                    pass
    except Exception as e:
        print(f"Error parsing {t_path}: {e}")
        
    return title, created_ts, updated_ts, max(1, step_count)

def sync_conversations(db_path=None, dry_run=False, no_backup=False):
    """Scans all brain folders and merges any missing conversations into the SQLite DB."""
    if not db_path:
        db_path = get_ide_db_path()
        
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return
        
    if not no_backup and not dry_run:
        backup_db(db_path)
        
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT value FROM ItemTable WHERE key='antigravityUnifiedStateSync.trajectorySummaries'")
    row = cursor.fetchone()
    
    if row and row[0]:
        raw = base64.b64decode(row[0])
        # Auto-decode top layer so it handles the repeated list correctly
        msg, top_typedef = blackboxprotobuf.decode_message(raw)
    else:
        print("No existing conversation history found! Creating a fresh index...")
        msg = {'1': []}
        top_typedef = TOP_TYPEDEF
        
    # Get set of all currently indexed UUIDs
    indexed_uuids = set()
    for item in msg.get('1', []):
        cid = item.get('1', b'').decode('utf-8', errors='ignore')
        indexed_uuids.add(cid)
        
    print(f"Found {len(indexed_uuids)} conversations currently in the IDE index.")
    
    added_count = 0
    brain_dirs = get_brain_dirs()
    
    for brain_dir in brain_dirs:
        print(f"Scanning brain directory: {brain_dir}")
        for cid in os.listdir(brain_dir):
            if cid == 'tempmediaStorage' or cid == 'scratch' or cid in indexed_uuids:
                continue
                
            t_path = os.path.join(brain_dir, cid, '.system_generated', 'logs', 'transcript.jsonl')
            if not os.path.exists(t_path):
                continue
                
            title, created_ts, updated_ts, step_count = parse_transcript_metadata(t_path)
            
            print(f"  [+] Injecting missing chat: {cid} | {title}")
            
            if not dry_run:
                # Create the inner message structure
                inner_msg = create_inner_msg(cid, title, created_ts, updated_ts, step_count)
                
                # Encode inner message with strict INNER_TYPEDEF
                inner_bytes = blackboxprotobuf.encode_message(inner_msg, INNER_TYPEDEF)
                
                # Wrap it into the outer item
                new_item = {
                    '1': cid.encode('utf-8'),
                    '2': {
                        '1': base64.b64encode(inner_bytes) # The IDE expects base64 here!
                    }
                }
                
                if '1' not in msg:
                    msg['1'] = []
                msg['1'].insert(0, new_item) # Insert at top
                added_count += 1

    if dry_run:
        print("Dry run complete. No changes made.")
    elif added_count > 0:
        print(f"Re-encoding database payload with {added_count} new conversations...")
        new_bytes = blackboxprotobuf.encode_message(msg, top_typedef)
        new_b64 = base64.b64encode(new_bytes).decode('utf-8')
        
        cursor.execute(
            "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
            ('antigravityUnifiedStateSync.trajectorySummaries', new_b64)
        )
        conn.commit()
        print(f"Successfully saved {added_count} conversations to the index!")
    else:
        print("No missing conversations found. You are fully synced!")
        
    conn.close()
