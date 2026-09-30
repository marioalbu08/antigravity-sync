@echo off
echo =======================================================
echo Antigravity IDE Chat History Restorer ^& Sync Tool
echo =======================================================
echo.

python -c "import blackboxprotobuf" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Missing dependency. Installing 'blackboxprotobuf' via pip...
    pip install blackboxprotobuf --quiet
)

echo.
echo Launching Interactive Sync Tool...
python -m antigravity_sync.cli %*

echo.
pause
