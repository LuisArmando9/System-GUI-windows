import pythoncom

from win32com.client import GetObject


class ProcessPC:
    # se crea el objeto para acceder al  Windows Management Instrumentation
    def __init__(self):
        pythoncom.CoInitialize()
        self.wmi = GetObject(r'winmgmts:')
    @property
    def CPU(self):
        #SE GENERA UNA INSTACIA DE WMI
        cpu_class = self.wmi.InstancesOf('Win32_Processor')
        for cpu in cpu_class:
            return {'Nombre': cpu.Name,
                    'Nucleos': f'Nucleos: {cpu.NumberOfEnabledCore}',
                    'Hilos': f'Hilos: {cpu.NumberOfLogicalProcessors}',
                    'Porcentaje': cpu.LoadPercentage
                    }
    @property   
    def PROCESS_ACTIVE(self):
        process_active_class = self.wmi.InstancesOf('Win32_Process')
        list_services = []
        listnameservicestemp = []
        for process in process_active_class:
            if process.Caption not in listnameservicestemp:
                listnameservicestemp.append(process.Caption)
                list_services.append(
                    {
                    'NAMEPROCESS' : process.Caption,
                    'PID': process.Processid,
                    }
                )
        return list_services
        




pythoncom.CoUninitialize()