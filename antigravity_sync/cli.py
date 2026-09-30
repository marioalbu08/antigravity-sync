# antigravity_sync/cli.py
import argparse
import sys
import time
from .core import sync_conversations
from .utils import wait_for_ide_close, is_ide_running, get_ide_db_path, get_desktop_db_path
from .injector import inject_markdown_conversation

def print_banner():
    print("=" * 60)
    print("     Antigravity Chat History Restorer & Sync Tool     ")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Sync and restore missing Antigravity chat histories.")
    parser.add_argument('--watch', action='store_true', help='Wait for IDE to close, then sync automatically.')
    parser.add_argument('--dry-run', action='store_true', help='Simulate sync without modifying database.')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating a .vscdb backup.')
    parser.add_argument('--inject', type=str, help='Path to a Markdown file to inject as a conversation.')
    parser.add_argument('--sync-desktop', action='store_true', help='Target Desktop App database instead of IDE.')
    
    args = parser.parse_args()
    print_banner()
    
    if args.inject:
        inject_markdown_conversation(args.inject)
        return

    if args.watch:
        print("Watcher mode activated.")
        wait_for_ide_close()
        db_path = get_desktop_db_path() if args.sync_desktop else get_ide_db_path()
        sync_conversations(db_path=db_path, dry_run=args.dry_run, no_backup=args.no_backup)
        return

    if is_ide_running():
        print("\n[!] WARNING: Antigravity IDE is currently running!")
        print("Modifying the database while the IDE is open will result in changes being OVERWRITTEN when it closes.")
        choice = input("Do you want to wait for it to close? (Y/n): ").strip().lower()
        if choice != 'n':
            wait_for_ide_close()
        else:
            print("Proceeding anyway, but changes may be lost.")
            
    db_path = get_desktop_db_path() if args.sync_desktop else get_ide_db_path()
    sync_conversations(db_path=db_path, dry_run=args.dry_run, no_backup=args.no_backup)

if __name__ == '__main__':
    main()
