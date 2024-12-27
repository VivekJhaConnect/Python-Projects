import win32serviceutil
import win32service
import win32event
import servicemanager
import time
from file_monitor import Watcher


class FileMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FileMonitorService"
    _svc_display_name_ = "File Monitor Service"
    _svc_description_ = "A service to monitor file changes in a directory."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.watcher = Watcher()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.watcher.stop()

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ""))
        self.start_monitoring()

    def start_monitoring(self):
        self.watcher.run()

    def clear_events(self):
        self.watcher.clear_events()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FileMonitorService)