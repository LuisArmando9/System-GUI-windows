from PyQt5.QtGui import   QPainter, QPen, QFont, QColor, QColor 
from PyQt5.QtWidgets import  QLabel,QProgressBar, QVBoxLayout
from math import sqrt


class QTPROGRESSROUND(QProgressBar):
    def __init__(self, parent=None):
        super(QTPROGRESSROUND, self).__init__(parent)
        self.values = (self.value()*360)/100
        self.label = QLabel("<center>0%<center>")
        self.label.setStyleSheet("background-color:transparent;\n"
                                    "color:#00ffc1\n")
        self.label.setFont(QFont("courrier",20, 75))
        self.v = QVBoxLayout(self)
        self.setLayout(self.v)
        self.v.addWidget(self.label)
    def setValue(self,n):
        self.n = n
        self.values = ((n*5650)/100)*(-1)
        self.label.setText("<center>"+str(self.n)+"%</center>")
    #Se sobreescribe el metodo que permitira crear la barra de progreso redondeada
    def paintEvent(self,event):
         painter = QPainter(self)
         painter.setRenderHint(QPainter.Antialiasing)
         pen = QPen()
         pen.setWidth(9)
         pen.setColor(QColor("#191a2f"))
         painter.setPen(pen)
         painter.drawArc(5.1,5.1,self.width()-10,self.height()-10,1450,-5650)
         pen = QPen()
         pen.setWidth(10)
         pen.setColor(QColor("#00ffc1"))
         painter.setPen(pen)
         painter.drawArc(5.1,5.1,self.width()-10,self.height()-10,1450,self.values)
         self.update()