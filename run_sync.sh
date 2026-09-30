#!/usr/bin/env bash
echo "======================================================="
echo "Antigravity IDE Chat History Restorer & Sync Tool"
echo "======================================================="
echo ""

if ! python3 -c "import blackboxprotobuf" &> /dev/null; then
    echo "[!] Missing dependency. Installing 'blackboxprotobuf' via pip..."
    pip3 install blackboxprotobuf --quiet
fi

echo "Launching Interactive Sync Tool..."
python3 -m antigravity_sync.cli "$@"
