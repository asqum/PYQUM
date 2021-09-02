echo off
echo "MAKE SURE to DISABLE ANY OTHER SCPI SERVER BEFORE PROCEED..."
cd C:\Program Files\Keysight\M9347\bin

:: NO SPACE AROUND "="
set /p which=Selected up to M9347A-
ktM9347Scpi /c "%which:~,1%"

PAUSE