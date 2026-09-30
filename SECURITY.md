# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Actively supported |

## Reporting a Vulnerability

If you discover a security vulnerability in Antigravity Sync, please **do not** open a public GitHub Issue.

Instead, please report it privately by emailing: **aalexandru29matei@gmail.com**

You can expect:
- An acknowledgement within **48 hours**
- A fix or mitigation plan within **7 days**

## Security Considerations

- This tool modifies SQLite databases locally. It never transmits data over the network.
- Automatic backups are created before every write operation.
- No API keys, tokens, or credentials are required or stored.
- The tool only reads `.jsonl` transcript files from your local `.gemini/` directories.
