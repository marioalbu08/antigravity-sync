# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-09-30

### Added
- **Core Sync Engine**: Automatically scans `.gemini/` brain directories and restores missing conversations to the IDE's SQLite database.
- **Cross-App Merging**: Seamlessly merges histories between Antigravity Desktop App and Antigravity IDE.
- **AI Chat Injector**: Import Markdown files (from ChatGPT, Claude, etc.) as synthetic Antigravity transcripts using `--inject`.
- **Watcher Mode**: `--watch` flag blocks and waits for the IDE to close before modifying the database safely.
- **Dry Run Mode**: `--dry-run` flag simulates the sync without writing anything.
- **Automatic Backups**: Creates timestamped `.backup` copies of `state.vscdb` before every write operation.
- **Process Safety**: Detects if Antigravity IDE or Desktop App is running and warns the user before proceeding.
- **Desktop App Support**: `--sync-desktop` flag targets the standalone Antigravity Desktop App database.
- **Version Flag**: `--version` flag prints the current version.
- **Cross-Platform**: Full support for Windows, macOS, and Linux.
- **Launcher Scripts**: `run_sync.bat` (Windows) and `run_sync.sh` (macOS/Linux) with automatic dependency installation.
- **pip Install Support**: `setup.py` with console script entry point for global CLI installation.
