import servicemanager
import socket
import sys
import time
import win32event
import win32service
import win32serviceutil
import os
import ctypes

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"
    _svc_description_ = "My service description"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        servicemanager.LogInfoMsg("TestService - Service is stopped")

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        servicemanager.LogInfoMsg("TestService - Service is starting")
        
        try:
            self.main()
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg("TestService - Service is running")
        except Exception as e:
            servicemanager.LogErrorMsg(f"TestService - Error: {str(e)}")
            self.SvcStop()

    def main(self):
        rc = None
        while rc != win32event.WAIT_OBJECT_0:
            with open(r'C:\FileMonitor\TestService.log', 'a') as f:
                f.write('test service running...\n')
            servicemanager.LogInfoMsg("TestService - Service is writing to log")
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
        servicemanager.LogInfoMsg("TestService - Main loop is exiting")

if __name__ == '__main__':
    if not is_admin():
        print("This script must be run as an administrator.")
        sys.exit(1)

    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)
