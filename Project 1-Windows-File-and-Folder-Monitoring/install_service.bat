@echo off
REM Change to the directory where the Python script and virtual environment should be
cd C:\FileMonitor

REM Create a virtual environment named 'venv'
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install the watchdog package
pip install watchdog

REM Install the service
python file_monitor_service.py install

REM Start the service
python file_monitor_service.py start

echo Service installed and started.
pause
