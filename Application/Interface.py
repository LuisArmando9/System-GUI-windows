
autor = """

/$$$$$$      /$$$$$$  /$$$$$$$  /$$      /$$  /$$$$$$  /$$   /$$
/$$$__  $$$   /$$__  $$| $$__  $$| $$  /$ | $$ /$$__  $$| $$$ | $$
/$$_/  \_  $$ | $$  \ $$| $$  \ $$| $$ /$$$| $$| $$  \ $$| $$$$| $$
/$$/ /$$$$$  $$| $$$$$$$$| $$$$$$$/| $$/$$ $$ $$| $$$$$$$$| $$ $$ $$
| $$ /$$  $$| $$| $$__  $$| $$__  $$| $$$$_  $$$$| $$__  $$| $$  $$$$
| $$| $$\ $$| $$| $$  | $$| $$  \ $$| $$$/ \  $$$| $$  | $$| $$\  $$$
| $$|  $$$$$$$$/| $$  | $$| $$  | $$| $$/   \  $$| $$  | $$| $$ \  $$
|  $$\________/ |__/  |__/|__/  |__/|__/     \__/|__/  |__/|__/  \__/
\  $$$   /$$$                                                       
\_  $$$$$$_/                                                       
 \______/   

email: ah25632@gmail.com
"""

import sys, time
from math import ceil, pow
from threading import Thread
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
                                QHBoxLayout, QGridLayout, 
                                    QMainWindow, QLabel)
from PyQt5.QtCore import Qt,  QPoint, QRect, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap 
from contentgui.CONSTANTS import STYLES
from contentgui.progressbar import QTPROGRESSROUND
from system.powerStatus import BatteryInfo
from system.RAMDATA import dataMemory
from system.processes import ProcessPC

#se crea el hilo secundario para las barras de progreso
class THREAD_BARPROGRRES(QThread):
    def __init__ (self, parent=None, option = 'CPU'):
        QThread.__init__(self, parent)
        self.option = option
    #SE EMITE SEÑAL DE TIPO INT
    countChanged = pyqtSignal(int)
    def run(self):
        
        while True:
            #CAPTURA PORCENTAJES
            Percent_PROGRESS_BAR = { 'CPU':ProcessPC().CPU['Porcentaje'],
                                    'RAM': dataMemory().dwMemoryLoad,
                                    'POWER' : BatteryInfo().BatteryLifePercent
            }
            time.sleep(1)
            self.countChanged.emit(Percent_PROGRESS_BAR[self.option])

class Interface(QMainWindow):
        def __init__(self, parent=None):
                super(Interface, self).__init__(parent, Qt.FramelessWindowHint)
                self.setObjectName("Interface")
                self.setFixedSize(800, 430)
                self.setStyleSheet(STYLES)
                self.resize(824, 542)
                self.Postion =  QPoint()
                #progressbarr
                self.progress_cpu = QTPROGRESSROUND(self)
                self.progress_ram = QTPROGRESSROUND(self)
                self.progress_power = QTPROGRESSROUND(self)
                self.LOAD_PROGRESSBAR()
               
        def create_widget(self):
            self.progress_cpu.setGeometry(30, 60, 215, 215)
            self.progress_ram.setGeometry(255, 60, 215, 215)
            self.progress_power.setGeometry(480, 60, 215, 215)
            #buttons
            self.controlButtons()
            #label
            self.textControl()
        
           

        def textControl(self):
            processs_text = CONTENT_TEXT_PROCCESS()
            textCpu, textRAM, textPower = QLabel(self), QLabel(self), QLabel(self)
            textCpu.setGeometry(QRect(40, 285, 220, 90))
            textCpu.setText(processs_text['TEXT_CPU'])
            textCpu.setAlignment(Qt.AlignCenter)
            textRAM.setGeometry(QRect(250, 285, 220, 80))  
            textRAM.setText(processs_text['TEXT_RAM'])
            textRAM.setAlignment(Qt.AlignCenter)
            textPower.setGeometry(QRect(470, 285, 240, 80))  
            textPower.setText(processs_text['TEXT_POWER'])
            textPower.setAlignment(Qt.AlignCenter)
        #metodo para el control de los botones de cierre y minimizar
        def controlButtons(self):
            #buttons close, minimize
            buttonClose,  buttonMin  = QPushButton('', self), QPushButton('', self)
            #buttons close
            buttonClose.setStyleSheet("qproperty-icon: url(contentgui/Images/close.png);")
            buttonClose.setGeometry(QRect(740, 10, 30, 30))
            buttonClose.clicked.connect(lambda: sys.exit())
            #button minimizar
            buttonMin.setStyleSheet("qproperty-icon: url(contentgui/Images/minimizar.png);")
            buttonMin.setGeometry(QRect(700, 10, 30, 30))
            buttonMin.clicked.connect(lambda : self.setWindowState(Qt.WindowMinimized))
       #CREA LOS HILOS DE EJECUCION PARA LAS BARRAS DE PROGRESO
        def LOAD_PROGRESSBAR(self):
            THREAD_PROGRRESBAR_CPU = THREAD_BARPROGRRES(self, 'CPU')
            THREAD_PROGRRESBAR_RAM = THREAD_BARPROGRRES(self, 'RAM')
            THREAD_PROGRRESBAR_POWER = THREAD_BARPROGRRES(self,'POWER')
            THREAD_PROGRRESBAR_CPU.countChanged.connect(lambda value: self.progress_cpu.setValue(value) )
            THREAD_PROGRRESBAR_RAM.countChanged.connect(lambda value: self.progress_ram.setValue(value) )
            THREAD_PROGRRESBAR_POWER.countChanged.connect(lambda value: self.progress_power.setValue(value))
            THREAD_PROGRRESBAR_CPU.start()
            THREAD_PROGRRESBAR_RAM.start()
            THREAD_PROGRRESBAR_POWER.start()
    
            
        #sobreescribe los siguientes metodos para poder mover la ventana
        def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                        self.Position = event.globalPos() - self.frameGeometry().topLeft()
                        event.accept()

        def mouseMoveEvent(self, event):
                if event.buttons() == Qt.LeftButton:
                        self.move(event.globalPos() - self.Position)
                        event.accept()
                
def CONTENT_TEXT_PROCCESS():
    cpu_data = ProcessPC()
    #SE CALCULA EL TOTAL DE MEMORIA RAM
    memory_full = round(dataMemory().ullTotalPhys/pow(1024, 3), 1)
    power = BatteryInfo()
    status_power = ""
    """
    MAYOR INFORMACION SOBRE POWER https://docs.microsoft.com/es-es/windows/win32/api/winbase/ns-winbase-system_power_status
    """
    if power.ACLineStatus: 
         status_power = "Te conectado a la corriente"
    elif power.ACLineStatus == 255 :
         status_power = "No contienes bateria"
    else:
        status_power = " Tu bateria se encuentra  desconetada"
    
    return { 'TEXT_CPU': f""" CPU \n {cpu_data.CPU['Nombre'][:30]} \n  {cpu_data.CPU['Nucleos']}\n {cpu_data.CPU['Hilos']}""",
            'TEXT_RAM': f"""RAM \n Memoria Total: {ceil(memory_full)} GB \n Memoria Disponible: {memory_full}""",
            'TEXT_POWER': f"""Bateria \n {status_power}  \n La vida de tu bateria son:{int(power.BatteryLifeTime/(3600*24*365))} años"""
        }




if __name__ == "__main__":     
    app = QApplication(sys.argv)
    w = Interface()
    w.create_widget()
    w.show()
    sys.exit(app.exec_())


