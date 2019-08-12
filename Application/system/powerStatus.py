
from ctypes import (windll, Structure, c_byte, byref)
from ctypes.wintypes import DWORD

""""
 Crea una estructura por referencia con los siguientes valores
 
  BYTE  ACLineStatus;
  BYTE  BatteryFlag;
  BYTE  BatteryLifePercent;
  BYTE  SystemStatusFlag;
  DWORD BatteryLifeTime;
  DWORD BatteryFullLifeTime;
mas informacion https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getsystempowerstatus


"""

class SYSTEM_POWER_STATUS(Structure):
    BYTE = c_byte
    _fields_ = [('ACLineStatus', BYTE),
                ('BatteryFlag', BYTE),
                ('BatteryLifePercent', BYTE),
                ('SystemStatusFlag', BYTE),
                ('BatteryFullLifeTime', DWORD),
                ('BatteryLifeTime', DWORD)]
    
def BatteryInfo():
    #byref nos permite pasar algun dato por referencia en ctypes
    power = SYSTEM_POWER_STATUS()
    windll.Kernel32.GetSystemPowerStatus(byref(power))
    return power
 
   

   
