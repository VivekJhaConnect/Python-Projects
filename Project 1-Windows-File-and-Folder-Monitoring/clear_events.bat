@echo off
REM Change to the directory where the Python script and virtual environment are
cd C:\FileMonitor

REM Activate the virtual environment
call venv\Scripts\activate

REM Clear events by restarting the service
python file_monitor_service.py stop
python file_monitor_service.py start

echo Events cleared and observer rescheduled.
pause
