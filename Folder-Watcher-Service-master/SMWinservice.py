import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import time

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''
    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''ClassMethod to parse the command line'''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''Constructor of the winservice'''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''Called when the service is asked to stop'''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''Called when the service is asked to start'''
        # self.start()        
        # servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
        #                       servicemanager.PYS_SERVICE_STARTED,
        #                       (self._svc_name_, ''))
        # self.main()
        try:
            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
            servicemanager.LogInfoMsg("TestService - Service is starting")
            
            # Simulate some startup tasks
            time.sleep(5)
            
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            servicemanager.LogInfoMsg("TestService - Service is running")
            self.main()
        except Exception as e:
            servicemanager.LogErrorMsg(f"TestService - Error: {str(e)}")
            self.SvcStop()

    def start(self):
        '''Override to add logic before the start eg. running condition'''
        pass

    def stop(self):
        '''Override to add logic before the stop eg. invalidating running condition'''
        pass

    def main(self):
        '''Main class to be ovverridden to add logic'''
        pass

if __name__ == '__main__':
    SMWinservice.parse_command_line()