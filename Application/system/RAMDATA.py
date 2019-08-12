
import sys, time
from ctypes import (windll, Structure, byref, sizeof, c_ulonglong)
from ctypes.wintypes import DWORD
import math
DWORDLONG = c_ulonglong
#SE CREA UNA ESTRUCTURA PARA ACCEDER A LAS PROPIEDADES DE  LA MEMORIA
class MEMORYSTATUS(Structure):
    _fields_ = [
        ('dwLength', DWORD),
        ('dwMemoryLoad', DWORD),
        ('ullTotalPhys', DWORDLONG),
        ('ullAvailPhys', DWORDLONG),
        ('ullTotalPageFile', DWORDLONG),
        ('ullAvailPageFile', DWORDLONG),
        ('ullTotalVirtual', DWORDLONG),
        ('ullAvailVirtual',DWORDLONG),
        ('ullAvailExtendedVirtual', DWORDLONG)
        ]
    def __init__(self):
        #TAMAÑO DE BYTES QUE NECESITA EL PUNTERO
        self.dwLength = sizeof(self)
        
def dataMemory():
    memory = MEMORYSTATUS()
    windll.kernel32.GlobalMemoryStatusEx(byref(memory))
    return memory
