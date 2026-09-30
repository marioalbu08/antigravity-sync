# Antigravity Chat Sync & Restore 🚀

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![OS: Windows | macOS | Linux](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-success)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-yellow.svg)

Have your Antigravity chats mysteriously disappeared after an IDE update or reinstall? Or do you use both the Antigravity Desktop App and Antigravity IDE and hate that they don't share history?

**Antigravity Sync** is a powerful utility that safely recovers, merges, and syncs your conversation history databases. It reverse-engineers the undocumented Protobuf schema embedded within the VS Code SQLite state database to restore your chats precisely.

## Features ✨

* **Complete History Recovery**: Restores "ghost" chats whose UI index was deleted during an update but whose local JSONL transcripts still survive in the `.gemini/` brain folders.
* **Cross-App Merging**: Automatically merges histories between the standalone Desktop app and the IDE.
* **Cross-Platform**: Works natively on Windows, macOS, and Linux.
* **Zero Data-Loss Guarantee**: Automatically creates timestamped `.backup` copies of your `state.vscdb` before touching anything.
* **AI Chat Injector**: *[NEW!]* Import generic Markdown chats (from ChatGPT, Claude, etc.) directly into Antigravity so you can continue the conversation!
* **Watcher Mode**: Blocks and waits for you to cleanly exit Antigravity IDE so it doesn't overwrite your restored database.

## Quick Start 🛠️

1. Close **Antigravity IDE** (if it's running).
2. Download or clone this repository.
3. Simply run the launcher for your OS:
   - **Windows:** Double-click `run_sync.bat`
   - **macOS / Linux:** Run `./run_sync.sh`

*Note: The script will automatically install its only dependency (`blackboxprotobuf`) if you don't have it.*

## Advanced CLI Options 💻

If you want to run it manually or build automation scripts:

```bash
python -m antigravity_sync.cli [OPTIONS]
```

| Flag | Description |
|---|---|
| `--watch` | Watcher mode: Automatically waits for the Antigravity IDE process to exit before modifying the DB. |
| `--dry-run` | Safe simulation mode. Scans your system and prints exactly what it *would* inject without actually modifying the database. |
| `--no-backup` | Skips creating a `.backup` of `state.vscdb` (not recommended). |
| `--sync-desktop` | Applies changes to the standalone Antigravity Desktop app database instead of the IDE database. |
| `--inject <file.md>` | **AI Chat Injector:** Provide a path to a Markdown file containing a chat, and the tool will synthetically convert it into an Antigravity transcript and inject it into your UI! |

## Injecting Markdown Chats (AI Chat Injector) 💉

Got a great prompt chain in ChatGPT or Claude that you want to bring into Antigravity IDE?
Save it as `my_cool_chat.md` and run:

```bash
python -m antigravity_sync.cli --inject my_cool_chat.md
```

Next time you open Antigravity, you'll see "my_cool_chat" in your history!

## Why do chats disappear? 🔍

Antigravity IDE is built on top of VS Code. The UI list of "Recent Conversations" is actually cached entirely inside a binary Protobuf blob inside VS Code's internal SQLite database (`AppData/Roaming/Antigravity IDE/User/globalStorage/state.vscdb`), specifically under the key `antigravityUnifiedStateSync.trajectorySummaries`.

When you uninstall, update, or clear the IDE cache, this SQLite database is wiped. However, the *actual* chat transcripts (the heavy JSONL files) are safely stored in your home directory (`~/.gemini/antigravity-ide/brain/`). Because the UI index is wiped, Antigravity "forgets" that the files exist. This tool simply regenerates the Protobuf UI index from the surviving files!

## Safety Note ⚠️

Antigravity IDE locks the SQLite database into memory while running, and saves it to disk when closing. If you run this tool while the IDE is open, your changes will be overwritten the second you close the IDE. Always close the IDE first, or use the `--watch` flag.

## License
MIT
