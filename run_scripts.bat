@echo off
:: Force English language
chcp 437 > nul
set LANG=en_US

:: Set the working directory
cd /d C:\Users\drews\CTC_MLProject

:: Create required directories if they don't exist
if not exist "scapy_packet_files" mkdir scapy_packet_files
if not exist "scapy_processed_files" mkdir scapy_processed_files

:: Start dump.py in a new terminal window
echo Starting dump.py...
start "Dump Script" cmd /k "chcp 437 > nul && cd /d C:\Users\drews\CTC_MLProject && python dump.py"

:: Wait a moment for the server to start
timeout /t 2 /nobreak > nul

:: Start monitor.py in a new terminal window
echo Starting monitor.py...
start "Monitor Script" cmd /k "chcp 437 > nul && cd /d C:\Users\drews\CTC_MLProject && python monitor.py"

echo.
echo Both scripts are running in separate windows.
echo Close the terminal windows to stop the scripts.
echo Press Ctrl+C to exit this window.
cmd /k